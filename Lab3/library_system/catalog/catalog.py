from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import FIELD_ID, RULE_UNIQUE
from ..exceptions import ItemNotFoundError, ValidationError

if TYPE_CHECKING:
    from .author import Author
    from .category import Category
    from .item_copy import ItemCopy
    from .library_item import LibraryItem


class Catalog:
    """Каталог изданий, рубрик и авторов."""

    def __init__(self):
        self.items: dict[str, LibraryItem] = {}
        self.categories: dict[str, Category] = {}
        self.authors: dict[str, Author] = {}

    def add_item(self, item: LibraryItem) -> None:
        """Добавляет издание; идентификатор должен быть уникальным."""
        if item.item_id in self.items:
            raise ValidationError(FIELD_ID, RULE_UNIQUE)
        self.items[item.item_id] = item

    def get_item(self, item_id: str) -> LibraryItem:
        """Возвращает издание по идентификатору."""
        if item_id not in self.items:
            raise ItemNotFoundError(item_id)
        return self.items[item_id]

    def remove_item(self, item_id: str) -> LibraryItem:
        """Удаляет издание из каталога и возвращает его."""
        item = self.get_item(item_id)
        del self.items[item_id]
        return item

    def add_category(self, category: Category) -> None:
        """Регистрирует рубрику."""
        self.categories[category.category_id] = category

    def add_author(self, author: Author) -> None:
        """Регистрирует автора."""
        self.authors[author.author_id] = author

    def find_copy(self, inventory_number: str) -> ItemCopy:
        """Находит экземпляр по инвентарному номеру."""
        for item in self.items.values():
            for copy in item.copies:
                if copy.inventory_number == inventory_number:
                    return copy
        raise ItemNotFoundError(inventory_number)

    def search_by_title(self, fragment: str) -> list[LibraryItem]:
        """Ищет издания по части названия."""
        needle = fragment.strip().lower()
        return [item for item in self.items.values() if needle in item.title.lower()]

    def search_by_author(self, name: str) -> list[LibraryItem]:
        """Ищет издания по части имени автора."""
        needle = name.strip().lower()
        return [item for item in self.items.values() if needle in item.author_names().lower()]

    def search_by_category(self, category: Category) -> list[LibraryItem]:
        """Возвращает издания рубрики и вложенных рубрик."""
        return [
            item
            for item in self.items.values()
            if item.category is not None and category.includes(item.category)
        ]

    def available_items(self) -> list[LibraryItem]:
        """Возвращает издания, у которых есть свободные экземпляры."""
        return [item for item in self.items.values() if item.has_available_copy()]

    def recent_items(self, current_year: int) -> list[LibraryItem]:
        """Возвращает недавно вышедшие издания."""
        return [item for item in self.items.values() if item.is_recent(current_year)]
