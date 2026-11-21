from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID
from ..validation import require_text

if TYPE_CHECKING:
    from ..people.reader import Reader
    from .library_event import LibraryEvent


class EventRegistration:
    """Запись читателя на мероприятие."""

    def __init__(
        self, registration_id: str, event: LibraryEvent, reader: Reader, registered_on: date
    ):
        self.registration_id = require_text(registration_id, FIELD_ID)
        self.event = event
        self.reader = reader
        self.registered_on = registered_on
        self.attended = False
        self.is_cancelled = False

    def is_active(self) -> bool:
        """Проверяет, что запись не отменена."""
        return not self.is_cancelled

    def cancel(self) -> None:
        """Отменяет запись."""
        self.is_cancelled = True

    def mark_attended(self) -> None:
        """Отмечает присутствие читателя на мероприятии."""
        self.attended = self.is_active()
