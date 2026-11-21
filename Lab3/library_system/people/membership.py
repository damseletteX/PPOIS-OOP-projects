from __future__ import annotations

from datetime import date, timedelta

from ..constants import (
    DAYS_IN_YEAR,
    FIELD_DAYS,
    MEMBERSHIP_FEES,
    MEMBERSHIP_LOAN_LIMITS,
)
from ..enums import MembershipPlan
from ..validation import require_positive


class Membership:
    """Абонемент читателя: тариф, срок действия и оплаченный взнос."""

    def __init__(self, plan: MembershipPlan, started_on: date):
        self.plan = plan
        self.started_on = started_on
        self.valid_until = started_on + timedelta(days=DAYS_IN_YEAR)
        self.fee_paid = MEMBERSHIP_FEES[plan]
        self.is_suspended = False

    def is_valid_on(self, on_date: date) -> bool:
        """Проверяет, действует ли абонемент на дату."""
        return not self.is_suspended and on_date <= self.valid_until

    def loan_limit(self) -> int:
        """Возвращает лимит одновременных выдач по тарифу."""
        return MEMBERSHIP_LOAN_LIMITS[self.plan]

    def days_left(self, on_date: date) -> int:
        """Возвращает число оставшихся дней действия."""
        return max(0, (self.valid_until - on_date).days)

    def extend(self, days: int) -> None:
        """Продлевает абонемент на указанное число дней."""
        require_positive(days, FIELD_DAYS)
        self.valid_until += timedelta(days=days)

    def upgrade(self, new_plan: MembershipPlan) -> float:
        """Меняет тариф и возвращает доплату (для понижения тарифа — ноль)."""
        surcharge = max(0.0, MEMBERSHIP_FEES[new_plan] - MEMBERSHIP_FEES[self.plan])
        self.plan = new_plan
        self.fee_paid += surcharge
        return surcharge

    def suspend(self) -> None:
        """Приостанавливает абонемент."""
        self.is_suspended = True

    def resume(self) -> None:
        """Возобновляет абонемент."""
        self.is_suspended = False
