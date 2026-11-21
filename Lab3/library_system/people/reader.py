from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..catalog.review import Review
from ..constants import (
    FIELD_ID,
    REASON_INACTIVE,
    REASON_NO_CARD,
)
from ..enums import MembershipPlan
from ..exceptions import AgeRestrictionError, ReaderBlockedError
from ..validation import require_text
from .library_card import LibraryCard
from .membership import Membership
from .person import Person
from .reading_list import ReadingList

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem
    from ..circulation.loan import Loan
    from ..circulation.reservation import Reservation
    from ..finance.fine import Fine


class Reader(Person):
    """Читатель библиотеки."""

    def __init__(
        self,
        reader_id: str,
        name: str,
        phone: str,
        birth_date: date,
        registered_on: date,
        email: str = "",
    ):
        super().__init__(name, phone, birth_date, email)
        self.reader_id = require_text(reader_id, FIELD_ID)
        self.registered_on = registered_on
        self.membership = Membership(MembershipPlan.BASIC, registered_on)
        self.card: LibraryCard | None = None
        self.loans: list[Loan] = []
        self.reservations: list[Reservation] = []
        self.fines: list[Fine] = []
        self.reading_list: ReadingList | None = None

    def issue_card(self, card_number: str, on_date: date) -> LibraryCard:
        """Оформляет читательский билет."""
        self.card = LibraryCard(card_number, self, on_date)
        return self.card

    def block_card(self, reason: str) -> None:
        """Блокирует читательский билет."""
        self._require_card().block(reason)

    def unblock_card(self) -> None:
        """Снимает блокировку читательского билета."""
        self._require_card().unblock()

    def renew_card(self, on_date: date) -> LibraryCard:
        """Продлевает читательский билет."""
        card = self._require_card()
        card.renew(on_date)
        return card

    def ensure_card_valid(self, on_date: date) -> None:
        """Проверяет, что читатель может пользоваться библиотекой."""
        if not self.is_active:
            raise ReaderBlockedError(self.name, REASON_INACTIVE)
        if self.card is None:
            raise ReaderBlockedError(self.name, REASON_NO_CARD)
        self.card.ensure_usable(on_date)

    def ensure_may_read(self, item: LibraryItem, on_date: date) -> None:
        """Проверяет возрастное ограничение издания."""
        if not item.is_suitable_for_age(self.age_on(on_date)):
            raise AgeRestrictionError(item.title, item.age_limit)

    def loan_limit(self) -> int:
        """Возвращает лимит одновременных выдач."""
        return self.membership.loan_limit()

    def loan_bonus_days(self) -> int:
        """Возвращает дополнительные дни к сроку выдачи."""
        return 0

    def change_plan(self, plan: MembershipPlan) -> float:
        """Меняет тариф абонемента и возвращает доплату."""
        return self.membership.upgrade(plan)

    def add_loan(self, loan: Loan) -> None:
        """Записывает выдачу в историю читателя."""
        self.loans.append(loan)

    def add_reservation(self, reservation: Reservation) -> None:
        """Записывает бронь в историю читателя."""
        self.reservations.append(reservation)

    def add_fine(self, fine: Fine) -> None:
        """Записывает штраф в историю читателя."""
        self.fines.append(fine)

    def active_loans(self) -> list[Loan]:
        """Возвращает невозвращённые выдачи."""
        return [loan for loan in self.loans if loan.is_active()]

    def overdue_loans(self, on_date: date) -> list[Loan]:
        """Возвращает просроченные выдачи на дату."""
        return [loan for loan in self.active_loans() if loan.is_overdue(on_date)]

    def unpaid_fines_total(self) -> float:
        """Возвращает сумму неоплаченных штрафов."""
        return sum(fine.balance() for fine in self.fines)

    def write_review(
        self, review_id: str, item: LibraryItem, rating: int, text: str, on_date: date
    ) -> Review:
        """Оставляет отзыв об издании."""
        review = Review(review_id, item, self, rating, text, on_date)
        item.add_review(review)
        return review

    def create_reading_list(self, list_id: str, title: str, on_date: date) -> ReadingList:
        """Создаёт список «хочу прочитать»."""
        self.reading_list = ReadingList(list_id, self, title, on_date)
        return self.reading_list

    def _require_card(self) -> LibraryCard:
        if self.card is None:
            raise ReaderBlockedError(self.name, REASON_NO_CARD)
        return self.card
