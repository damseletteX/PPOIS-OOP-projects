from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_NAME, FIELD_YEAR
from ..validation import require_positive, require_text

if TYPE_CHECKING:
    from .library_item import LibraryItem


class Publisher:
    """Издательство."""

    def __init__(self, publisher_id: str, name: str, city: str, founded_year: int):
        self.publisher_id = require_text(publisher_id, FIELD_ID)
        self.name = require_text(name, FIELD_NAME)
        self.city = require_text(city, FIELD_NAME)
        self.founded_year = require_positive(founded_year, FIELD_YEAR)
        self.items: list[LibraryItem] = []

    def publish(self, item: LibraryItem) -> None:
        """Регистрирует издание за издательством."""
        if item not in self.items:
            self.items.append(item)

    def items_published_in(self, year: int) -> list[LibraryItem]:
        """Возвращает издания, вышедшие в указанном году."""
        return [item for item in self.items if item.year == year]

    def age_in(self, year: int) -> int:
        """Возвращает возраст издательства в указанный год."""
        return max(0, year - self.founded_year)

    def catalog_size(self) -> int:
        """Возвращает число изданий издательства в каталоге."""
        return len(self.items)
