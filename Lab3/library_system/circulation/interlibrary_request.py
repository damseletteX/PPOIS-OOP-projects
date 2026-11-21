from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    ENTITY_REQUEST,
    FIELD_ID,
    FIELD_TITLE,
    INTERLIBRARY_FEE,
)
from ..enums import RequestStatus
from ..validation import ensure_transition, require_text

if TYPE_CHECKING:
    from ..people.librarian import Librarian
    from ..people.reader import Reader


class InterlibraryRequest:
    """Запрос читателя на издание из другой библиотеки (МБА)."""

    def __init__(
        self,
        request_id: str,
        reader: Reader,
        title: str,
        partner_library: str,
        requested_on: date,
    ):
        self.request_id = require_text(request_id, FIELD_ID)
        self.reader = reader
        self.title = require_text(title, FIELD_TITLE)
        self.partner_library = require_text(partner_library, FIELD_TITLE)
        self.requested_on = requested_on
        self.status = RequestStatus.REQUESTED
        self.handled_by: Librarian | None = None
        self.expected_on: date | None = None
        self.fee = 0.0

    def approve(self, librarian: Librarian, expected_on: date) -> None:
        """Одобряет запрос и назначает плату за доставку."""
        self._move_to(RequestStatus.APPROVED, {RequestStatus.REQUESTED})
        self.handled_by = librarian
        self.expected_on = expected_on
        self.fee = INTERLIBRARY_FEE

    def reject(self, librarian: Librarian) -> None:
        """Отклоняет запрос."""
        self._move_to(RequestStatus.REJECTED, {RequestStatus.REQUESTED})
        self.handled_by = librarian

    def mark_received(self) -> None:
        """Отмечает, что издание получено из другой библиотеки."""
        self._move_to(RequestStatus.RECEIVED, {RequestStatus.APPROVED})

    def is_overdue(self, on_date: date) -> bool:
        """Проверяет, что ожидаемая дата поставки прошла."""
        is_waiting = self.status == RequestStatus.APPROVED
        return is_waiting and self.expected_on is not None and on_date > self.expected_on

    def days_waiting(self, on_date: date) -> int:
        """Возвращает, сколько дней запрос ожидает исполнения."""
        return (on_date - self.requested_on).days

    def _move_to(self, target: RequestStatus, allowed: set[RequestStatus]) -> None:
        ensure_transition(ENTITY_REQUEST, self.status, allowed, target)
        self.status = target
