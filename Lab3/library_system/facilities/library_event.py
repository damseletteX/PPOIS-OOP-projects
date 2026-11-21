from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    FIELD_CAPACITY,
    FIELD_ID,
    FIELD_TITLE,
    REASON_ALREADY_REGISTERED,
    REASON_EVENT_CANCELLED,
)
from ..exceptions import CapacityExceededError, ReservationError
from ..validation import require_positive, require_text
from .event_registration import EventRegistration

if TYPE_CHECKING:
    from ..people.reader import Reader
    from ..people.staff import Staff
    from .reading_room import ReadingRoom


class LibraryEvent:
    """Мероприятие библиотеки: встреча, лекция, мастер-класс."""

    def __init__(
        self,
        event_id: str,
        title: str,
        event_date: date,
        room: ReadingRoom,
        organizer: Staff,
        max_participants: int,
    ):
        require_positive(max_participants, FIELD_CAPACITY)
        if max_participants > room.seats_total:
            raise CapacityExceededError(room.name, room.seats_total)
        self.event_id = require_text(event_id, FIELD_ID)
        self.title = require_text(title, FIELD_TITLE)
        self.event_date = event_date
        self.room = room
        self.organizer = organizer
        self.max_participants = max_participants
        self.registrations: list[EventRegistration] = []
        self.is_cancelled = False

    def attendees_count(self) -> int:
        """Возвращает число действующих записей."""
        return sum(1 for registration in self.registrations if registration.is_active())

    def seats_left(self) -> int:
        """Возвращает число свободных мест."""
        return self.max_participants - self.attendees_count()

    def is_full(self) -> bool:
        """Проверяет, что мест не осталось."""
        return self.seats_left() <= 0

    def is_upcoming(self, on_date: date) -> bool:
        """Проверяет, что мероприятие ещё не прошло и не отменено."""
        return not self.is_cancelled and self.event_date >= on_date

    def register_reader(
        self, registration_id: str, reader: Reader, on_date: date
    ) -> EventRegistration:
        """Записывает читателя на мероприятие."""
        if self.is_cancelled:
            raise ReservationError(REASON_EVENT_CANCELLED)
        if self._find_active(reader) is not None:
            raise ReservationError(REASON_ALREADY_REGISTERED)
        if self.is_full():
            raise CapacityExceededError(self.title, self.max_participants)
        registration = EventRegistration(registration_id, self, reader, on_date)
        self.registrations.append(registration)
        return registration

    def cancel_registration(self, reader: Reader) -> None:
        """Отменяет запись читателя."""
        registration = self._find_active(reader)
        if registration is not None:
            registration.cancel()

    def cancel_event(self) -> None:
        """Отменяет мероприятие."""
        self.is_cancelled = True

    def _find_active(self, reader: Reader) -> EventRegistration | None:
        for registration in self.registrations:
            if registration.reader is reader and registration.is_active():
                return registration
        return None
