from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import CURRENCY_DIGITS, ENTITY_ORDER, FIELD_ID
from ..enums import OrderStatus
from ..validation import ensure_transition, require_text

if TYPE_CHECKING:
    from ..people.director import Director
    from .purchase_line import PurchaseLine
    from .supplier import Supplier


class PurchaseOrder:
    """Заказ поставщику на пополнение фонда."""

    def __init__(self, order_id: str, supplier: Supplier, created_on: date):
        self.order_id = require_text(order_id, FIELD_ID)
        self.supplier = supplier
        self.created_on = created_on
        self.lines: list[PurchaseLine] = []
        self.status = OrderStatus.DRAFT
        self.approved_by: Director | None = None
        self.expected_on: date | None = None
        supplier.add_order(self)

    def add_line(self, line: PurchaseLine) -> None:
        """Добавляет позицию в черновик заказа."""
        ensure_transition(ENTITY_ORDER, self.status, {OrderStatus.DRAFT}, OrderStatus.DRAFT)
        self.lines.append(line)

    def total_cost(self) -> float:
        """Возвращает стоимость заказа."""
        return round(sum(line.total() for line in self.lines), CURRENCY_DIGITS)

    def items_count(self) -> int:
        """Возвращает общее число заказанных экземпляров."""
        return sum(line.quantity for line in self.lines)

    def mark_approved(self, director: Director) -> None:
        """Фиксирует утверждение заказа директором."""
        self._move_to(OrderStatus.APPROVED, {OrderStatus.DRAFT})
        self.approved_by = director

    def send(self, on_date: date) -> None:
        """Отправляет утверждённый заказ поставщику."""
        self._move_to(OrderStatus.SENT, {OrderStatus.APPROVED})
        self.expected_on = self.supplier.expected_delivery(on_date)

    def receive_line(self, line: PurchaseLine, quantity: int) -> None:
        """Принимает поставку по позиции; полностью принятый заказ закрывается."""
        ensure_transition(ENTITY_ORDER, self.status, {OrderStatus.SENT}, OrderStatus.RECEIVED)
        line.receive(quantity)
        if all(item.is_fully_received() for item in self.lines):
            self.status = OrderStatus.RECEIVED

    def cancel(self) -> None:
        """Отменяет заказ, пока он не получен."""
        allowed = {OrderStatus.DRAFT, OrderStatus.APPROVED, OrderStatus.SENT}
        self._move_to(OrderStatus.CANCELLED, allowed)

    def is_overdue(self, on_date: date) -> bool:
        """Проверяет, что поставка задерживается."""
        is_sent = self.status == OrderStatus.SENT
        return is_sent and self.expected_on is not None and on_date > self.expected_on

    def _move_to(self, target: OrderStatus, allowed: set[OrderStatus]) -> None:
        ensure_transition(ENTITY_ORDER, self.status, allowed, target)
        self.status = target
