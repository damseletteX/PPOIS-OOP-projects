from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import (
    ACTION_DELIVERY,
    DAYS_IN_MONTH,
    ENTITY_SUBSCRIPTION,
    FIELD_ID,
    FIELD_QUANTITY,
    STATE_CANCELLED,
)
from ..exceptions import InvalidStatusTransitionError
from ..validation import require_positive, require_text

if TYPE_CHECKING:
    from ..catalog.magazine import Magazine
    from ..people.reader import Reader


class Subscription:
    """Подписка читателя на периодическое издание."""

    def __init__(
        self,
        subscription_id: str,
        reader: Reader,
        magazine: Magazine,
        start_on: date,
        months: int,
    ):
        require_positive(months, FIELD_QUANTITY)
        self.subscription_id = require_text(subscription_id, FIELD_ID)
        self.reader = reader
        self.magazine = magazine
        self.start_on = start_on
        self.end_on = start_on + timedelta(days=months * DAYS_IN_MONTH)
        self.delivered_issues = 0
        self.is_cancelled = False

    def is_active_on(self, on_date: date) -> bool:
        """Проверяет, действует ли подписка на дату."""
        return not self.is_cancelled and self.start_on <= on_date <= self.end_on

    def cancel(self) -> None:
        """Отменяет подписку."""
        self.is_cancelled = True

    def renew(self, months: int) -> None:
        """Продлевает подписку на число месяцев."""
        require_positive(months, FIELD_QUANTITY)
        self.end_on += timedelta(days=months * DAYS_IN_MONTH)

    def deliver_issue(self) -> int:
        """Фиксирует доставку выпуска и возвращает общее число доставленных."""
        if self.is_cancelled:
            raise InvalidStatusTransitionError(
                ENTITY_SUBSCRIPTION, STATE_CANCELLED, ACTION_DELIVERY
            )
        self.delivered_issues += 1
        return self.delivered_issues

    def days_left(self, on_date: date) -> int:
        """Возвращает число оставшихся дней подписки."""
        return max(0, (self.end_on - on_date).days)
