from __future__ import annotations

from datetime import date, datetime, time

from ..constants import (
    DAYS_IN_WEEK,
    DEFAULT_CLOSE_TIME,
    DEFAULT_OPEN_TIME,
    DEFAULT_WORKING_WEEKDAYS,
    FIELD_TIME,
    RULE_BEFORE_END,
)
from ..exceptions import ValidationError
from ..timeutils import hours_between


class OpeningHours:
    """График работы филиала или зала."""

    def __init__(
        self,
        open_time: time = DEFAULT_OPEN_TIME,
        close_time: time = DEFAULT_CLOSE_TIME,
        working_weekdays: frozenset[int] = DEFAULT_WORKING_WEEKDAYS,
    ):
        if open_time >= close_time:
            raise ValidationError(FIELD_TIME, RULE_BEFORE_END)
        self.open_time = open_time
        self.close_time = close_time
        self.working_weekdays = working_weekdays

    def is_working_day(self, on_date: date) -> bool:
        """Проверяет, что в этот день недели библиотека работает."""
        return on_date.weekday() in self.working_weekdays

    def is_open_at(self, moment: datetime) -> bool:
        """Проверяет, открыто ли в указанный момент."""
        in_hours = self.open_time <= moment.time() < self.close_time
        return self.is_working_day(moment.date()) and in_hours

    def daily_hours(self) -> float:
        """Возвращает длительность рабочего дня в часах."""
        return hours_between(self.open_time, self.close_time)

    def working_days_count(self) -> int:
        """Возвращает число рабочих дней в неделе."""
        return len(self.working_weekdays)

    def weekly_hours(self) -> float:
        """Возвращает рабочие часы в неделю."""
        return self.daily_hours() * self.working_days_count()

    def next_working_day(self, on_date: date) -> date | None:
        """Находит ближайший рабочий день, начиная со следующего."""
        for offset in range(1, DAYS_IN_WEEK + 1):
            candidate = date.fromordinal(on_date.toordinal() + offset)
            if self.is_working_day(candidate):
                return candidate
        return None
