from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import (
    MESSAGE_OVERDUE_REMINDER,
    MESSAGE_RESERVATION_READY,
    REASON_AVAILABLE_NOW,
    REASON_HAS_QUEUE,
    REASON_LOAN_CLOSED,
    REASON_OVERDUE,
    REASON_RENEWAL_LIMIT,
    RESERVATION_HOLD_DAYS,
)
from ..enums import CopyCondition, FineReason, IdKind
from ..exceptions import (
    ItemNotAvailableError,
    ItemNotFoundError,
    LoanLimitExceededError,
    OverdueLoansError,
    RenewalNotAllowedError,
    ReservationError,
    UnpaidFineError,
)
from ..finance.fine import Fine
from ..finance.fine_policy import FinePolicy
from ..ids import IdGenerator
from .loan import Loan
from .loan_policy import LoanPolicy
from .lost_item_report import LostItemReport
from .notification import Notification
from .renewal import Renewal
from .reservation import Reservation
from .return_record import ReturnRecord
from .waiting_list import WaitingList

if TYPE_CHECKING:
    from ..catalog.item_copy import ItemCopy
    from ..catalog.library_item import LibraryItem
    from ..people.librarian import Librarian
    from ..people.reader import Reader
    from ..people.staff import Staff


class LoanDesk:
    """Кафедра выдачи: оформляет выдачу, возврат, продление и бронирование."""

    def __init__(
        self,
        ids: IdGenerator,
        loan_policy: LoanPolicy | None = None,
        fine_policy: FinePolicy | None = None,
    ):
        self.ids = ids
        self.loan_policy = loan_policy or LoanPolicy()
        self.fine_policy = fine_policy or FinePolicy()
        self.loans: list[Loan] = []
        self.returns: list[ReturnRecord] = []
        self.fines: list[Fine] = []
        self.lost_reports: list[LostItemReport] = []
        self.waiting_lists: dict[str, WaitingList] = {}
        self.ready_reservations: list[Reservation] = []
        self.notifications: list[Notification] = []

    def find_loan(self, loan_id: str) -> Loan:
        """Находит выдачу по идентификатору."""
        for loan in self.loans:
            if loan.loan_id == loan_id:
                return loan
        raise ItemNotFoundError(loan_id)

    def waiting_list_for(self, item: LibraryItem) -> WaitingList:
        """Возвращает очередь на издание, создавая её при необходимости."""
        if item.item_id not in self.waiting_lists:
            self.waiting_lists[item.item_id] = WaitingList(item)
        return self.waiting_lists[item.item_id]

    def issue_loan(
        self, reader: Reader, copy: ItemCopy, librarian: Librarian, on_date: date
    ) -> Loan:
        """Выдаёт экземпляр читателю после проверки всех условий."""
        self._ensure_reader_eligible(reader, copy.item, on_date)
        if not copy.is_available_for(reader):
            raise ItemNotAvailableError(copy.item.title)
        due_on = self.loan_policy.due_date_for(reader, copy.item, on_date)
        loan = Loan(self.ids.next_id(IdKind.LOAN), reader, copy, librarian, on_date, due_on)
        copy.mark_loaned()
        self._fulfill_ready_reservation(reader, copy.item)
        reader.add_loan(loan)
        librarian.register_issued_loan(loan)
        self.loans.append(loan)
        return loan

    def accept_return(
        self, loan: Loan, condition: CopyCondition, receiver: Librarian, on_date: date
    ) -> ReturnRecord:
        """Принимает издание, начисляет штрафы и передаёт экземпляр следующему в очереди."""
        loan.close(on_date)
        loan.copy.mark_returned(condition)
        record = ReturnRecord(self.ids.next_id(IdKind.RETURN), loan, on_date, condition, receiver)
        self._charge_fines(record)
        self._hold_for_next_reader(loan.copy, on_date)
        self.returns.append(record)
        return record

    def renew_loan(self, loan: Loan, approver: Staff, on_date: date) -> Renewal:
        """Продлевает выдачу, если это разрешено правилами."""
        self._ensure_renewable(loan, on_date)
        new_due_on = loan.due_on + timedelta(days=self.loan_policy.renewal_days)
        renewal = Renewal(self.ids.next_id(IdKind.RENEWAL), loan, on_date, new_due_on)
        renewal.approve(approver)
        loan.extend(renewal)
        return renewal

    def reserve_item(self, reader: Reader, item: LibraryItem, on_date: date) -> Reservation:
        """Ставит читателя в очередь на издание, у которого нет свободных экземпляров."""
        reader.ensure_card_valid(on_date)
        if item.has_available_copy():
            raise ReservationError(REASON_AVAILABLE_NOW)
        reservation = Reservation(self.ids.next_id(IdKind.RESERVATION), reader, item, on_date)
        self.waiting_list_for(item).enqueue(reservation)
        reader.add_reservation(reservation)
        return reservation

    def cancel_reservation(self, reservation: Reservation, on_date: date) -> None:
        """Отменяет бронь и освобождает отложенный экземпляр."""
        was_ready = reservation in self.ready_reservations
        reservation.cancel()
        self.waiting_list_for(reservation.item).remove(reservation)
        if was_ready:
            self.ready_reservations.remove(reservation)
            self._release_held_copy(reservation, on_date)

    def expire_reservations(self, on_date: date) -> int:
        """Закрывает брони, не востребованные в срок; возвращает их число."""
        expired = [item for item in self.ready_reservations if item.expire_if_needed(on_date)]
        for reservation in expired:
            self.ready_reservations.remove(reservation)
            self._release_held_copy(reservation, on_date)
        return len(expired)

    def report_lost(self, loan: Loan, on_date: date) -> LostItemReport:
        """Оформляет утрату издания и начисляет компенсацию."""
        loan.mark_lost()
        loan.copy.mark_lost()
        amount = self.fine_policy.loss_fine(loan.copy.price)
        fine = self._add_fine(loan, amount, FineReason.LOSS, on_date)
        report = LostItemReport(self.ids.next_id(IdKind.REPORT), loan, on_date, fine)
        self.lost_reports.append(report)
        return report

    def collect_overdue_loans(self, on_date: date) -> list[Loan]:
        """Возвращает все просроченные выдачи."""
        return [loan for loan in self.loans if loan.is_overdue(on_date)]

    def send_overdue_reminders(self, on_date: date) -> list[Notification]:
        """Отправляет напоминания должникам."""
        reminders = []
        for loan in self.collect_overdue_loans(on_date):
            text = MESSAGE_OVERDUE_REMINDER.format(
                title=loan.copy.item.title, due_on=loan.due_on.isoformat()
            )
            reminders.append(self._notify(loan.reader, text, on_date))
        return reminders

    def _ensure_reader_eligible(self, reader: Reader, item: LibraryItem, on_date: date) -> None:
        reader.ensure_card_valid(on_date)
        reader.ensure_may_read(item, on_date)
        if not item.is_loanable():
            raise ItemNotAvailableError(item.title)
        limit = self.loan_policy.effective_loan_limit(reader)
        if len(reader.active_loans()) >= limit:
            raise LoanLimitExceededError(reader.name, limit)
        overdue = reader.overdue_loans(on_date)
        if overdue:
            raise OverdueLoansError(reader.name, len(overdue))
        unpaid_total = reader.unpaid_fines_total()
        if self.loan_policy.blocks_borrowing(unpaid_total):
            raise UnpaidFineError(reader.name, unpaid_total)

    def _ensure_renewable(self, loan: Loan, on_date: date) -> None:
        if not loan.is_active():
            raise RenewalNotAllowedError(REASON_LOAN_CLOSED)
        if loan.is_overdue(on_date):
            raise RenewalNotAllowedError(REASON_OVERDUE)
        if not self.loan_policy.can_renew(loan):
            raise RenewalNotAllowedError(REASON_RENEWAL_LIMIT)
        waiting = self.waiting_lists.get(loan.copy.item.item_id)
        if waiting is not None and not waiting.is_empty():
            raise RenewalNotAllowedError(REASON_HAS_QUEUE)

    def _fulfill_ready_reservation(self, reader: Reader, item: LibraryItem) -> None:
        for reservation in self.ready_reservations:
            if reservation.reader is reader and reservation.item is item:
                reservation.fulfill()
                self.ready_reservations.remove(reservation)
                return

    def _charge_fines(self, record: ReturnRecord) -> None:
        overdue_amount = self.fine_policy.overdue_fine(record.days_late())
        if overdue_amount > 0:
            self._add_fine(record.loan, overdue_amount, FineReason.OVERDUE, record.returned_on)
        damage_amount = self.fine_policy.damage_fine(record.condition, record.loan.copy.price)
        if damage_amount > 0:
            self._add_fine(record.loan, damage_amount, FineReason.DAMAGE, record.returned_on)

    def _add_fine(self, loan: Loan, amount: float, reason: FineReason, on_date: date) -> Fine:
        fine = Fine(self.ids.next_id(IdKind.FINE), loan.reader, loan, amount, reason, on_date)
        loan.reader.add_fine(fine)
        self.fines.append(fine)
        return fine

    def _hold_for_next_reader(self, copy: ItemCopy, on_date: date) -> None:
        waiting = self.waiting_lists.get(copy.item.item_id)
        reservation = waiting.pop_next() if waiting is not None else None
        if reservation is None:
            return
        copy.mark_reserved(reservation.reader)
        reservation.mark_ready(on_date)
        self.ready_reservations.append(reservation)
        text = MESSAGE_RESERVATION_READY.format(title=copy.item.title, days=RESERVATION_HOLD_DAYS)
        self._notify(reservation.reader, text, on_date)

    def _release_held_copy(self, reservation: Reservation, on_date: date) -> None:
        for copy in reservation.item.copies:
            if copy.reserved_for is reservation.reader:
                copy.release_reservation()
                self._hold_for_next_reader(copy, on_date)
                return

    def _notify(self, reader: Reader, message: str, on_date: date) -> Notification:
        notification = Notification(self.ids.next_id(IdKind.NOTIFICATION), reader, message, on_date)
        self.notifications.append(notification)
        return notification
