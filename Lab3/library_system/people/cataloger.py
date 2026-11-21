from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from .staff import Staff

if TYPE_CHECKING:
    from ..catalog.catalog import Catalog
    from ..catalog.category import Category
    from ..catalog.library_item import LibraryItem


class Cataloger(Staff):
    """Каталогизатор, вносящий издания в каталог."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        phone: str,
        birth_date: date,
        salary: float,
        hired_on: date,
        email: str = "",
    ):
        super().__init__(staff_id, name, phone, birth_date, salary, hired_on, email)
        self.cataloged_items: list[LibraryItem] = []
        self.specialization: Category | None = None

    def set_specialization(self, category: Category) -> None:
        """Назначает основную тематику работы."""
        self.specialization = category

    def catalog_item(self, catalog: Catalog, item: LibraryItem) -> None:
        """Вносит издание в каталог и запоминает это."""
        catalog.add_item(item)
        self.cataloged_items.append(item)

    def classify_item(self, item: LibraryItem, category: Category) -> None:
        """Присваивает изданию рубрику."""
        item.assign_category(category)

    def cataloged_count(self) -> int:
        """Возвращает число внесённых изданий."""
        return len(self.cataloged_items)

    def specializes_in(self, category: Category) -> bool:
        """Проверяет, входит ли рубрика в тематику каталогизатора."""
        return self.specialization is not None and self.specialization.includes(category)
