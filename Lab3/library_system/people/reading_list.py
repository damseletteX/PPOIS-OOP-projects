from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_TITLE, RULE_UNIQUE
from ..exceptions import ValidationError
from ..validation import require_text

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem
    from .reader import Reader


class ReadingList:
    """Список изданий, которые читатель хочет прочитать."""

    def __init__(self, list_id: str, owner: Reader, title: str, created_on: date):
        self.list_id = require_text(list_id, FIELD_ID)
        self.owner = owner
        self.title = require_text(title, FIELD_TITLE)
        self.created_on = created_on
        self.items: list[LibraryItem] = []
        self.is_public = False

    def add_item(self, item: LibraryItem) -> None:
        """Добавляет издание, если его ещё нет в списке."""
        if self.contains(item):
            raise ValidationError(FIELD_TITLE, RULE_UNIQUE)
        self.items.append(item)

    def remove_item(self, item: LibraryItem) -> None:
        """Убирает издание из списка."""
        if self.contains(item):
            self.items.remove(item)

    def contains(self, item: LibraryItem) -> bool:
        """Проверяет, есть ли издание в списке."""
        return item in self.items

    def available_items(self) -> list[LibraryItem]:
        """Возвращает издания списка, которые сейчас можно взять."""
        return [item for item in self.items if item.has_available_copy()]

    def total_items(self) -> int:
        """Возвращает число изданий в списке."""
        return len(self.items)

    def make_public(self) -> None:
        """Делает список доступным другим читателям."""
        self.is_public = True

    def make_private(self) -> None:
        """Скрывает список от других читателей."""
        self.is_public = False
