from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import ENTITY_RESERVATION, FIELD_DAYS, FIELD_ID, RESERVATION_HOLD_DAYS
from ..enums import ReservationStatus
from ..validation import ensure_transition, require_positive, require_text

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem
    from ..people.reader import Reader


class Reservation:
    """Бронь издания читателем."""

    def __init__(self, reservation_id: str, reader: Reader, item: LibraryItem, created_on: date):
        self.reservation_id = require_text(reservation_id, FIELD_ID)
        self.reader = reader
        self.item = item
        self.created_on = created_on
        self.expires_on = created_on + timedelta(days=RESERVATION_HOLD_DAYS)
        self.status = ReservationStatus.ACTIVE

    def is_open(self) -> bool:
        """Проверяет, что бронь ещё не закрыта."""
        return self.status in {ReservationStatus.ACTIVE, ReservationStatus.READY}

    def mark_ready(self, on_date: date) -> None:
        """Сообщает, что экземпляр отложен, и отсчитывает срок хранения."""
        self._move_to(ReservationStatus.READY, {ReservationStatus.ACTIVE})
        self.expires_on = on_date + timedelta(days=RESERVATION_HOLD_DAYS)

    def fulfill(self) -> None:
        """Закрывает бронь после выдачи."""
        self._move_to(ReservationStatus.FULFILLED, {ReservationStatus.READY})

    def cancel(self) -> None:
        """Отменяет бронь."""
        self._move_to(
            ReservationStatus.CANCELLED, {ReservationStatus.ACTIVE, ReservationStatus.READY}
        )

    def expire_if_needed(self, on_date: date) -> bool:
        """Помечает готовую бронь истёкшей, если срок хранения прошёл."""
        is_expired = self.status == ReservationStatus.READY and on_date > self.expires_on
        if is_expired:
            self.status = ReservationStatus.EXPIRED
        return is_expired

    def extend(self, days: int) -> None:
        """Продлевает срок хранения."""
        require_positive(days, FIELD_DAYS)
        self.expires_on += timedelta(days=days)

    def days_until_expiry(self, on_date: date) -> int:
        """Возвращает число дней до окончания срока хранения."""
        return max(0, (self.expires_on - on_date).days)

    def _move_to(self, target: ReservationStatus, allowed: set[ReservationStatus]) -> None:
        ensure_transition(ENTITY_RESERVATION, self.status, allowed, target)
        self.status = target
