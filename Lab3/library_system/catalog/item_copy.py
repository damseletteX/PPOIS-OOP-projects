from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    FIELD_ID,
    FIELD_PRICE,
    ITEM_TYPE_COPY,
    LOANS_PER_WEAR_STEP,
    WEAR_PROGRESSION,
)
from ..enums import CopyCondition, CopyStatus
from ..exceptions import InvalidStatusTransitionError
from ..validation import require_non_negative, require_text

if TYPE_CHECKING:
    from ..facilities.shelf import Shelf
    from ..people.reader import Reader
    from .library_item import LibraryItem


class ItemCopy:
    """Физический экземпляр издания."""

    def __init__(
        self,
        inventory_number: str,
        item: LibraryItem,
        price: float,
        acquired_on: date,
        condition: CopyCondition = CopyCondition.NEW,
    ):
        self.inventory_number = require_text(inventory_number, FIELD_ID)
        self.item = item
        self.price = require_non_negative(price, FIELD_PRICE)
        self.acquired_on = acquired_on
        self.condition = condition
        self.status = CopyStatus.AVAILABLE
        self.shelf: Shelf | None = None
        self.reserved_for: Reader | None = None
        self.loans_count = 0

    def is_available(self) -> bool:
        """Проверяет, что экземпляр лежит на полке и никому не забронирован."""
        return self.status == CopyStatus.AVAILABLE

    def is_available_for(self, reader: Reader) -> bool:
        """Проверяет, что экземпляр можно выдать именно этому читателю."""
        reserved_for_reader = self.status == CopyStatus.RESERVED and self.reserved_for is reader
        return self.is_available() or reserved_for_reader

    def mark_loaned(self) -> None:
        """Переводит экземпляр в статус «на руках»."""
        self._move_to(CopyStatus.LOANED, {CopyStatus.AVAILABLE, CopyStatus.RESERVED})
        self.reserved_for = None
        self.loans_count += 1

    def mark_returned(self, condition: CopyCondition) -> None:
        """Принимает экземпляр обратно с указанием состояния."""
        self._move_to(CopyStatus.AVAILABLE, {CopyStatus.LOANED})
        self.condition = condition
        self._wear_if_due()

    def mark_reserved(self, reader: Reader) -> None:
        """Откладывает экземпляр для читателя из очереди."""
        self._move_to(CopyStatus.RESERVED, {CopyStatus.AVAILABLE})
        self.reserved_for = reader

    def release_reservation(self) -> None:
        """Возвращает отложенный экземпляр в свободный фонд."""
        self._move_to(CopyStatus.AVAILABLE, {CopyStatus.RESERVED})
        self.reserved_for = None

    def mark_lost(self) -> None:
        """Отмечает экземпляр утерянным."""
        self._move_to(CopyStatus.LOST, {CopyStatus.LOANED, CopyStatus.AVAILABLE})

    def write_off(self) -> None:
        """Списывает экземпляр из фонда."""
        allowed = {CopyStatus.AVAILABLE, CopyStatus.LOST, CopyStatus.RESERVED}
        self._move_to(CopyStatus.WRITTEN_OFF, allowed)
        self.reserved_for = None

    def needs_repair(self) -> bool:
        """Проверяет, что экземпляр повреждён."""
        return self.condition == CopyCondition.DAMAGED

    def assign_shelf(self, shelf: Shelf) -> None:
        """Запоминает полку хранения."""
        self.shelf = shelf

    def _move_to(self, target: CopyStatus, allowed: set[CopyStatus]) -> None:
        if self.status not in allowed:
            raise InvalidStatusTransitionError(ITEM_TYPE_COPY, self.status.value, target.value)
        self.status = target

    def _wear_if_due(self) -> None:
        is_wear_step = self.loans_count % LOANS_PER_WEAR_STEP == 0
        if is_wear_step and self.condition in WEAR_PROGRESSION:
            self.condition = WEAR_PROGRESSION[self.condition]
