from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_TIME, RULE_BEFORE_END
from ..exceptions import ValidationError
from ..timeutils import hours_between, intervals_overlap
from ..validation import require_text

if TYPE_CHECKING:
    from ..people.reader import Reader
    from .opening_hours import OpeningHours
    from .reading_room import ReadingRoom


class SeatBooking:
    """Бронь места в читальном зале."""

    def __init__(
        self,
        booking_id: str,
        reader: Reader,
        room: ReadingRoom,
        booking_date: date,
        start_time: time,
        end_time: time,
    ):
        if start_time >= end_time:
            raise ValidationError(FIELD_TIME, RULE_BEFORE_END)
        self.booking_id = require_text(booking_id, FIELD_ID)
        self.reader = reader
        self.room = room
        self.booking_date = booking_date
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = True

    def cancel(self) -> None:
        """Отменяет бронь."""
        self.is_active = False

    def duration_hours(self) -> float:
        """Возвращает длительность брони в часах."""
        return hours_between(self.start_time, self.end_time)

    def overlaps(self, on_date: date, start: time, end: time) -> bool:
        """Проверяет, что активная бронь пересекается с интервалом."""
        same_day = self.booking_date == on_date
        return (
            self.is_active
            and same_day
            and intervals_overlap(self.start_time, self.end_time, start, end)
        )

    def is_within_hours(self, hours: OpeningHours) -> bool:
        """Проверяет, что бронь укладывается в часы работы."""
        fits = hours.open_time <= self.start_time and self.end_time <= hours.close_time
        return hours.is_working_day(self.booking_date) and fits
