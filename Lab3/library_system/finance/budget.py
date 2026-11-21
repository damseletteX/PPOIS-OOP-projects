from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import CURRENCY_DIGITS, FIELD_AMOUNT, FIELD_ID, FIELD_YEAR, PERCENT_BASE
from ..exceptions import BudgetExceededError
from ..validation import require_positive, require_text

if TYPE_CHECKING:
    from .purchase_order import PurchaseOrder


class Budget:
    """Годовой бюджет комплектования фонда."""

    def __init__(self, budget_id: str, year: int, limit_amount: float):
        self.budget_id = require_text(budget_id, FIELD_ID)
        self.year = require_positive(year, FIELD_YEAR)
        self.limit_amount = require_positive(limit_amount, FIELD_AMOUNT)
        self.spent_amount = 0.0
        self.orders: list[PurchaseOrder] = []

    def remaining(self) -> float:
        """Возвращает остаток бюджета."""
        return round(self.limit_amount - self.spent_amount, CURRENCY_DIGITS)

    def usage_percent(self) -> float:
        """Возвращает долю израсходованных средств в процентах."""
        return round(self.spent_amount / self.limit_amount * PERCENT_BASE, CURRENCY_DIGITS)

    def is_exhausted(self) -> bool:
        """Проверяет, что бюджет исчерпан."""
        return self.remaining() <= 0

    def reserve(self, amount: float) -> None:
        """Резервирует средства под закупку."""
        require_positive(amount, FIELD_AMOUNT)
        if amount > self.remaining():
            raise BudgetExceededError(amount, self.remaining())
        self.spent_amount += amount

    def release(self, amount: float) -> None:
        """Возвращает зарезервированные средства в бюджет."""
        self.spent_amount = max(0.0, self.spent_amount - require_positive(amount, FIELD_AMOUNT))

    def increase_limit(self, amount: float) -> None:
        """Увеличивает лимит бюджета."""
        self.limit_amount += require_positive(amount, FIELD_AMOUNT)

    def add_order(self, order: PurchaseOrder) -> None:
        """Привязывает заказ к бюджету."""
        if order not in self.orders:
            self.orders.append(order)
