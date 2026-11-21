from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import CURRENCY_DIGITS, FIELD_CAPACITY, FIELD_ID, PERCENT_BASE
from ..exceptions import CapacityExceededError
from ..validation import require_positive, require_text

if TYPE_CHECKING:
    from ..catalog.category import Category
    from ..catalog.item_copy import ItemCopy
    from ..catalog.library_item import LibraryItem


class Shelf:
    """Полка хранения экземпляров."""

    def __init__(self, shelf_code: str, capacity: int, category: Category | None = None):
        self.shelf_code = require_text(shelf_code, FIELD_ID)
        self.capacity = require_positive(capacity, FIELD_CAPACITY)
        self.category = category
        self.copies: list[ItemCopy] = []

    def free_slots(self) -> int:
        """Возвращает число свободных мест."""
        return self.capacity - len(self.copies)

    def is_full(self) -> bool:
        """Проверяет, что свободных мест нет."""
        return self.free_slots() <= 0

    def occupancy_percent(self) -> float:
        """Возвращает заполненность полки в процентах."""
        return round(len(self.copies) / self.capacity * PERCENT_BASE, CURRENCY_DIGITS)

    def place_copy(self, copy: ItemCopy) -> None:
        """Ставит экземпляр на полку."""
        if self.is_full():
            raise CapacityExceededError(self.shelf_code, self.capacity)
        self.copies.append(copy)
        copy.assign_shelf(self)

    def remove_copy(self, copy: ItemCopy) -> None:
        """Снимает экземпляр с полки."""
        if copy in self.copies:
            self.copies.remove(copy)
            copy.shelf = None

    def contains_item(self, item: LibraryItem) -> bool:
        """Проверяет, есть ли на полке экземпляр издания."""
        return any(copy.item is item for copy in self.copies)
