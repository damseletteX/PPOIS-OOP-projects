from __future__ import annotations

from ..constants import (
    CURRENCY_DIGITS,
    DAMAGE_FINE_PERCENT,
    FINE_DAILY_RATE,
    FINE_GRACE_DAYS,
    FINE_MAX_AMOUNT,
    LOSS_PRICE_MULTIPLIER,
    LOSS_PROCESSING_FEE,
    PERCENT_BASE,
)
from ..enums import CopyCondition


class FinePolicy:
    """Тарифы штрафов за просрочку, повреждение и утрату."""

    def __init__(
        self,
        daily_rate: float = FINE_DAILY_RATE,
        grace_days: int = FINE_GRACE_DAYS,
        max_fine: float = FINE_MAX_AMOUNT,
    ):
        self.daily_rate = daily_rate
        self.grace_days = grace_days
        self.max_fine = max_fine

    def is_in_grace_period(self, days_overdue: int) -> bool:
        """Проверяет, что просрочка укладывается в льготный период."""
        return days_overdue <= self.grace_days

    def cap(self, amount: float) -> float:
        """Ограничивает сумму штрафа максимумом."""
        return min(amount, self.max_fine)

    def overdue_fine(self, days_overdue: int) -> float:
        """Возвращает штраф за просрочку с учётом льготных дней."""
        billable_days = max(0, days_overdue - self.grace_days)
        return round(self.cap(billable_days * self.daily_rate), CURRENCY_DIGITS)

    def damage_fine(self, condition: CopyCondition, price: float) -> float:
        """Возвращает штраф за повреждение как долю стоимости экземпляра."""
        percent = DAMAGE_FINE_PERCENT.get(condition, 0)
        return round(price * percent / PERCENT_BASE, CURRENCY_DIGITS)

    def loss_fine(self, price: float) -> float:
        """Возвращает компенсацию за утрату: кратная стоимость плюс сбор."""
        return round(price * LOSS_PRICE_MULTIPLIER + LOSS_PROCESSING_FEE, CURRENCY_DIGITS)
