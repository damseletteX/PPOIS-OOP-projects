from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_NAME, PATH_SEPARATOR
from ..validation import require_text

if TYPE_CHECKING:
    from .library_item import LibraryItem


class Category:
    """Рубрика каталога; рубрики образуют дерево."""

    def __init__(self, category_id: str, name: str, parent: Category | None = None):
        self.category_id = require_text(category_id, FIELD_ID)
        self.name = require_text(name, FIELD_NAME)
        self.parent = parent
        self.children: list[Category] = []
        self.items: list[LibraryItem] = []
        if parent is not None:
            parent.children.append(self)

    def add_item(self, item: LibraryItem) -> None:
        """Добавляет издание в рубрику."""
        if item not in self.items:
            self.items.append(item)

    def is_root(self) -> bool:
        """Проверяет, что у рубрики нет родителя."""
        return self.parent is None

    def path_names(self) -> list[str]:
        """Возвращает названия рубрик от корня до текущей."""
        names = []
        node: Category | None = self
        while node is not None:
            names.append(node.name)
            node = node.parent
        return list(reversed(names))

    def full_path(self) -> str:
        """Возвращает путь рубрики строкой."""
        return PATH_SEPARATOR.join(self.path_names())

    def depth(self) -> int:
        """Возвращает глубину вложенности (корень — ноль)."""
        return len(self.path_names()) - 1

    def includes(self, other: Category) -> bool:
        """Проверяет, совпадает ли рубрика с другой или является её предком."""
        node: Category | None = other
        while node is not None:
            if node is self:
                return True
            node = node.parent
        return False

    def all_items(self) -> list[LibraryItem]:
        """Возвращает издания рубрики и всех вложенных рубрик."""
        collected = list(self.items)
        for child in self.children:
            collected.extend(child.all_items())
        return collected
