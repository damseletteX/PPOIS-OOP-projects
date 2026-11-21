from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import DEFAULT_APPROVAL_LIMIT, FIELD_AMOUNT
from ..exceptions import BudgetExceededError
from ..validation import require_positive
from .staff import Staff

if TYPE_CHECKING:
    from ..finance.budget import Budget
    from ..finance.purchase_order import PurchaseOrder


class Director(Staff):
    """Директор библиотеки, утверждающий закупки."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        phone: str,
        birth_date: date,
        salary: float,
        hired_on: date,
        approval_limit: float = DEFAULT_APPROVAL_LIMIT,
        email: str = "",
    ):
        super().__init__(staff_id, name, phone, birth_date, salary, hired_on, email)
        self.approval_limit = require_positive(approval_limit, FIELD_AMOUNT)
        self.approved_orders: list[PurchaseOrder] = []

    def can_approve(self, order: PurchaseOrder) -> bool:
        """Проверяет, укладывается ли заказ в лимит полномочий."""
        return order.total_cost() <= self.approval_limit

    def approve_order(self, order: PurchaseOrder, budget: Budget) -> None:
        """Утверждает заказ и резервирует его стоимость в бюджете."""
        if not self.can_approve(order):
            raise BudgetExceededError(order.total_cost(), self.approval_limit)
        budget.reserve(order.total_cost())
        order.mark_approved(self)
        self.approved_orders.append(order)

    def reject_order(self, order: PurchaseOrder) -> None:
        """Отклоняет заказ."""
        order.cancel()

    def raise_limit(self, amount: float) -> None:
        """Увеличивает лимит полномочий."""
        self.approval_limit += require_positive(amount, FIELD_AMOUNT)

    def approved_total(self) -> float:
        """Возвращает суммарную стоимость утверждённых заказов."""
        return sum(order.total_cost() for order in self.approved_orders)
