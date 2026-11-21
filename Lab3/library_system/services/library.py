from __future__ import annotations

from datetime import date

from ..catalog.catalog import Catalog
from ..catalog.item_copy import ItemCopy
from ..circulation.loan import Loan
from ..circulation.loan_desk import LoanDesk
from ..circulation.lost_item_report import LostItemReport
from ..circulation.renewal import Renewal
from ..circulation.reservation import Reservation
from ..circulation.return_record import ReturnRecord
from ..constants import (
    DEFAULT_ROOM_NAME,
    DEFAULT_ROOM_SEATS,
    DEFAULT_SHELF_CAPACITY,
    FIELD_ADDRESS,
    FIELD_NAME,
    LABEL_BRANCHES,
    LABEL_FINES_OPEN,
    LABEL_ITEMS,
    LABEL_LOANS_ACTIVE,
    LABEL_READERS,
    LABEL_STAFF,
)
from ..enums import CopyCondition, IdKind, PaymentMethod
from ..exceptions import BudgetExceededError, ItemNotFoundError
from ..facilities.branch import Branch
from ..facilities.opening_hours import OpeningHours
from ..facilities.reading_room import ReadingRoom
from ..facilities.shelf import Shelf
from ..finance.budget import Budget
from ..finance.fine import Fine
from ..finance.payment import Payment
from ..finance.purchase_line import PurchaseLine
from ..finance.purchase_order import PurchaseOrder
from ..finance.supplier import Supplier
from ..ids import IdGenerator
from ..people.reader import Reader
from ..people.staff import Staff
from ..validation import require_text
from .library_report import LibraryReport
from .reader_registry import ReaderRegistry
from .reader_services import ReaderServices
from .staff_registry import StaffRegistry


class Library:
    """Библиотека: единая точка доступа к каталогу, читателям, выдаче и закупкам."""

    def __init__(self, name: str, address: str):
        self.name = require_text(name, FIELD_NAME)
        self.address = require_text(address, FIELD_ADDRESS)
        self.ids = IdGenerator()
        self.catalog = Catalog()
        self.readers = ReaderRegistry()
        self.staff = StaffRegistry()
        self.loan_desk = LoanDesk(self.ids)
        self.branches: dict[str, Branch] = {}
        self.suppliers: dict[str, Supplier] = {}
        self.orders: dict[str, PurchaseOrder] = {}
        self.payments: list[Payment] = []
        self.budget: Budget | None = None
        self.services = ReaderServices(self)

    def add_branch(self, branch: Branch) -> None:
        """Регистрирует филиал."""
        self.branches[branch.branch_id] = branch

    def get_branch(self, branch_id: str) -> Branch:
        """Возвращает филиал по идентификатору."""
        if branch_id not in self.branches:
            raise ItemNotFoundError(branch_id)
        return self.branches[branch_id]

    def open_branch(self, name: str, address: str, phone: str) -> Branch:
        """Открывает филиал со стандартным графиком, читальным залом и полкой."""
        branch_id = self.ids.next_id(IdKind.BRANCH)
        branch = Branch(branch_id, name, address, phone, OpeningHours())
        room = ReadingRoom(
            self.ids.next_id(IdKind.ROOM),
            DEFAULT_ROOM_NAME,
            DEFAULT_ROOM_SEATS,
            branch.opening_hours,
        )
        branch.add_room(room)
        branch.add_shelf(Shelf(self.ids.next_id(IdKind.SHELF), DEFAULT_SHELF_CAPACITY))
        self.add_branch(branch)
        return branch

    def hire_staff(self, staff: Staff, branch_id: str | None = None) -> None:
        """Принимает сотрудника на работу, при необходимости прикрепляя к филиалу."""
        self.staff.hire(staff)
        if branch_id is not None:
            self.get_branch(branch_id).hire(staff)

    def register_reader(self, reader: Reader, on_date: date) -> Reader:
        """Регистрирует читателя и сразу оформляет ему читательский билет."""
        self.readers.register(reader, on_date)
        reader.issue_card(self.ids.next_id(IdKind.CARD), on_date)
        return reader

    def receive_copy(self, item_id: str, branch_id: str, price: float, on_date: date) -> ItemCopy:
        """Заводит новый экземпляр издания и ставит его на свободную полку филиала."""
        item = self.catalog.get_item(item_id)
        shelf = self.get_branch(branch_id).find_free_shelf()
        copy = ItemCopy(self.ids.next_id(IdKind.COPY), item, price, on_date)
        shelf.place_copy(copy)
        item.add_copy(copy)
        return copy

    def issue_loan(
        self, reader_id: str, inventory_number: str, librarian_id: str, on_date: date
    ) -> Loan:
        """Выдаёт экземпляр читателю."""
        reader = self.readers.get(reader_id)
        copy = self.catalog.find_copy(inventory_number)
        librarian = self.staff.get_librarian(librarian_id)
        return self.loan_desk.issue_loan(reader, copy, librarian, on_date)

    def return_loan(
        self, loan_id: str, condition: CopyCondition, librarian_id: str, on_date: date
    ) -> ReturnRecord:
        """Принимает издание обратно."""
        loan = self.loan_desk.find_loan(loan_id)
        librarian = self.staff.get_librarian(librarian_id)
        return self.loan_desk.accept_return(loan, condition, librarian, on_date)

    def renew_loan(self, loan_id: str, staff_id: str, on_date: date) -> Renewal:
        """Продлевает выдачу."""
        loan = self.loan_desk.find_loan(loan_id)
        return self.loan_desk.renew_loan(loan, self.staff.get(staff_id), on_date)

    def reserve_item(self, reader_id: str, item_id: str, on_date: date) -> Reservation:
        """Бронирует издание для читателя."""
        reader = self.readers.get(reader_id)
        item = self.catalog.get_item(item_id)
        return self.loan_desk.reserve_item(reader, item, on_date)

    def report_lost(self, loan_id: str, on_date: date) -> LostItemReport:
        """Оформляет утрату издания."""
        loan = self.loan_desk.find_loan(loan_id)
        return self.loan_desk.report_lost(loan, on_date)

    def find_fine(self, reader_id: str, fine_id: str) -> Fine:
        """Находит штраф читателя по идентификатору."""
        for fine in self.readers.get(reader_id).fines:
            if fine.fine_id == fine_id:
                return fine
        raise ItemNotFoundError(fine_id)

    def pay_fine(
        self, reader_id: str, fine_id: str, amount: float, method: PaymentMethod, on_date: date
    ) -> Payment:
        """Принимает оплату штрафа."""
        fine = self.find_fine(reader_id, fine_id)
        payment_id = self.ids.next_id(IdKind.PAYMENT)
        payment = Payment(payment_id, fine.reader, fine, amount, method, on_date)
        payment.process()
        self.payments.append(payment)
        return payment

    def set_budget(self, year: int, limit_amount: float) -> Budget:
        """Создаёт бюджет комплектования на год."""
        self.budget = Budget(self.ids.next_id(IdKind.BUDGET), year, limit_amount)
        return self.budget

    def add_supplier(self, supplier: Supplier) -> None:
        """Регистрирует поставщика."""
        self.suppliers[supplier.supplier_id] = supplier

    def get_supplier(self, supplier_id: str) -> Supplier:
        """Возвращает поставщика по идентификатору."""
        if supplier_id not in self.suppliers:
            raise ItemNotFoundError(supplier_id)
        return self.suppliers[supplier_id]

    def require_budget(self) -> Budget:
        """Возвращает бюджет; если он не задан, средств для закупок нет."""
        if self.budget is None:
            raise BudgetExceededError(0.0, 0.0)
        return self.budget

    def create_order(self, supplier_id: str, on_date: date) -> PurchaseOrder:
        """Создаёт черновик заказа поставщику."""
        supplier = self.get_supplier(supplier_id)
        order = PurchaseOrder(self.ids.next_id(IdKind.ORDER), supplier, on_date)
        self.orders[order.order_id] = order
        return order

    def add_order_line(
        self, order_id: str, item_id: str, quantity: int, unit_price: float
    ) -> PurchaseLine:
        """Добавляет позицию в заказ."""
        line = PurchaseLine(self.catalog.get_item(item_id), quantity, unit_price)
        self.get_order(order_id).add_line(line)
        return line

    def get_order(self, order_id: str) -> PurchaseOrder:
        """Возвращает заказ по идентификатору."""
        if order_id not in self.orders:
            raise ItemNotFoundError(order_id)
        return self.orders[order_id]

    def approve_order(self, order_id: str, director_id: str) -> None:
        """Утверждает заказ директором и резервирует бюджет."""
        order = self.get_order(order_id)
        budget = self.require_budget()
        self.staff.get_director(director_id).approve_order(order, budget)
        budget.add_order(order)

    def send_order(self, order_id: str, on_date: date) -> None:
        """Отправляет утверждённый заказ поставщику."""
        self.get_order(order_id).send(on_date)

    def cancel_order(self, order_id: str) -> None:
        """Отменяет заказ и возвращает зарезервированные средства в бюджет."""
        order = self.get_order(order_id)
        was_reserved = order.approved_by is not None
        order.cancel()
        if was_reserved:
            self.require_budget().release(order.total_cost())

    def receive_order(self, order_id: str, branch_id: str, on_date: date) -> list[ItemCopy]:
        """Принимает поставку целиком и ставит новые экземпляры на полки."""
        order = self.get_order(order_id)
        received: list[ItemCopy] = []
        for line in order.lines:
            if not line.is_fully_received():
                received.extend(self._receive_line(order, line, branch_id, on_date))
        return received

    def _receive_line(
        self, order: PurchaseOrder, line: PurchaseLine, branch_id: str, on_date: date
    ) -> list[ItemCopy]:
        quantity = line.remaining()
        order.receive_line(line, quantity)
        item_id = line.item.item_id
        return [
            self.receive_copy(item_id, branch_id, line.unit_price, on_date) for _ in range(quantity)
        ]

    def generate_report(self, period_start: date, period_end: date) -> LibraryReport:
        """Формирует отчёт за период."""
        report_id = self.ids.next_id(IdKind.REPORT)
        desk = self.loan_desk
        return LibraryReport(
            report_id, period_start, period_end, desk.loans, desk.fines, self.payments
        )

    def summary(self) -> dict[str, str]:
        """Возвращает сводку о состоянии библиотеки."""
        open_fines = sum(1 for fine in self.loan_desk.fines if not fine.is_paid())
        return {
            LABEL_ITEMS: str(len(self.catalog.items)),
            LABEL_READERS: str(len(self.readers.readers)),
            LABEL_STAFF: str(len(self.staff.members)),
            LABEL_BRANCHES: str(len(self.branches)),
            LABEL_LOANS_ACTIVE: str(sum(1 for loan in self.loan_desk.loans if loan.is_active())),
            LABEL_FINES_OPEN: str(open_fines),
        }
