from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING

from ..constants import FIELD_CAPACITY, FIELD_ID, FIELD_NAME
from ..exceptions import CapacityExceededError
from ..validation import require_positive, require_text
from .seat_booking import SeatBooking

if TYPE_CHECKING:
    from ..people.reader import Reader
    from .opening_hours import OpeningHours


class ReadingRoom:
    """Читальный зал с бронированием мест."""

    def __init__(
        self,
        room_id: str,
        name: str,
        seats_total: int,
        opening_hours: OpeningHours,
        is_quiet_zone: bool = False,
    ):
        self.room_id = require_text(room_id, FIELD_ID)
        self.name = require_text(name, FIELD_NAME)
        self.seats_total = require_positive(seats_total, FIELD_CAPACITY)
        self.opening_hours = opening_hours
        self.is_quiet_zone = is_quiet_zone
        self.bookings: list[SeatBooking] = []

    def booked_seats(self, on_date: date, start: time, end: time) -> int:
        """Возвращает число занятых мест на интервал."""
        return sum(1 for booking in self.bookings if booking.overlaps(on_date, start, end))

    def free_seats(self, on_date: date, start: time, end: time) -> int:
        """Возвращает число свободных мест на интервал."""
        return self.seats_total - self.booked_seats(on_date, start, end)

    def is_full(self, on_date: date, start: time, end: time) -> bool:
        """Проверяет, что на интервал мест нет."""
        return self.free_seats(on_date, start, end) <= 0

    def book_seat(
        self, booking_id: str, reader: Reader, on_date: date, start: time, end: time
    ) -> SeatBooking:
        """Бронирует место, если зал открыт и есть свободные места."""
        booking = SeatBooking(booking_id, reader, self, on_date, start, end)
        if not booking.is_within_hours(self.opening_hours):
            raise CapacityExceededError(self.name, self.seats_total)
        if self.is_full(on_date, start, end):
            raise CapacityExceededError(self.name, self.seats_total)
        self.bookings.append(booking)
        return booking

    def cancel_booking(self, booking: SeatBooking) -> None:
        """Отменяет бронь места."""
        booking.cancel()

    def bookings_on(self, on_date: date) -> list[SeatBooking]:
        """Возвращает активные брони на день."""
        return [item for item in self.bookings if item.is_active and item.booking_date == on_date]
