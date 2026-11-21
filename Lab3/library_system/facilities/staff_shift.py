from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_TIME, RULE_BEFORE_END
from ..exceptions import ValidationError
from ..timeutils import hours_between, intervals_overlap
from ..validation import require_text

if TYPE_CHECKING:
    from ..people.staff import Staff
    from .branch import Branch


class StaffShift:
    """Рабочая смена сотрудника."""

    def __init__(
        self,
        shift_id: str,
        staff: Staff,
        branch: Branch,
        shift_date: date,
        start_time: time,
        end_time: time,
    ):
        if start_time >= end_time:
            raise ValidationError(FIELD_TIME, RULE_BEFORE_END)
        self.shift_id = require_text(shift_id, FIELD_ID)
        self.staff = staff
        self.branch = branch
        self.shift_date = shift_date
        self.start_time = start_time
        self.end_time = end_time

    def duration_hours(self) -> float:
        """Возвращает длительность смены в часах."""
        return hours_between(self.start_time, self.end_time)

    def overlaps(self, other: StaffShift) -> bool:
        """Проверяет пересечение с другой сменой."""
        same_day = self.shift_date == other.shift_date
        times = (self.start_time, self.end_time, other.start_time, other.end_time)
        return same_day and intervals_overlap(*times)

    def is_active_at(self, moment: datetime) -> bool:
        """Проверяет, идёт ли смена в указанный момент."""
        in_hours = self.start_time <= moment.time() < self.end_time
        return moment.date() == self.shift_date and in_hours
