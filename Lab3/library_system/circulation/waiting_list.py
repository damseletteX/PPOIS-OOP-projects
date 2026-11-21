from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import (
    MAX_QUEUE_LENGTH,
    REASON_ALREADY_QUEUED,
    REASON_QUEUE_FULL,
)
from ..enums import ReservationStatus
from ..exceptions import ReservationError

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem
    from ..people.reader import Reader
    from .reservation import Reservation


class WaitingList:
    """Очередь читателей на издание."""

    def __init__(self, item: LibraryItem, max_length: int = MAX_QUEUE_LENGTH):
        self.item = item
        self.max_length = max_length
        self.queue: list[Reservation] = []

    def enqueue(self, reservation: Reservation) -> int:
        """Ставит бронь в очередь и возвращает позицию читателя."""
        if self.position_of(reservation.reader):
            raise ReservationError(REASON_ALREADY_QUEUED)
        if len(self.queue) >= self.max_length:
            raise ReservationError(REASON_QUEUE_FULL)
        self.queue.append(reservation)
        return len(self.queue)

    def pop_next(self) -> Reservation | None:
        """Извлекает первую действующую бронь, пропуская отменённые."""
        while self.queue:
            reservation = self.queue.pop(0)
            if reservation.status == ReservationStatus.ACTIVE:
                return reservation
        return None

    def position_of(self, reader: Reader) -> int:
        """Возвращает позицию читателя (с единицы) или ноль, если его нет в очереди."""
        for position, reservation in enumerate(self.queue, start=1):
            if reservation.reader is reader and reservation.is_open():
                return position
        return 0

    def remove(self, reservation: Reservation) -> None:
        """Убирает бронь из очереди."""
        if reservation in self.queue:
            self.queue.remove(reservation)

    def size(self) -> int:
        """Возвращает длину очереди."""
        return len(self.queue)

    def is_empty(self) -> bool:
        """Проверяет, что очередь пуста."""
        return not self.queue
