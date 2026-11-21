from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_NAME, FIELD_YEAR, RULE_YEAR_ORDER
from ..exceptions import ValidationError
from ..validation import require_text

if TYPE_CHECKING:
    from .library_item import LibraryItem


class Author:
    """Автор произведений, представленных в каталоге."""

    def __init__(
        self,
        author_id: str,
        name: str,
        country: str,
        birth_year: int,
        death_year: int | None = None,
    ):
        if death_year is not None and death_year < birth_year:
            raise ValidationError(FIELD_YEAR, RULE_YEAR_ORDER)
        self.author_id = require_text(author_id, FIELD_ID)
        self.name = require_text(name, FIELD_NAME)
        self.country = require_text(country, FIELD_NAME)
        self.birth_year = birth_year
        self.death_year = death_year
        self.works: list[LibraryItem] = []

    def add_work(self, item: LibraryItem) -> None:
        """Добавляет произведение автору."""
        if item not in self.works:
            self.works.append(item)

    def remove_work(self, item: LibraryItem) -> None:
        """Убирает произведение из списка работ автора."""
        if item in self.works:
            self.works.remove(item)

    def works_count(self) -> int:
        """Возвращает число произведений автора в каталоге."""
        return len(self.works)

    def is_alive(self) -> bool:
        """Проверяет, жив ли автор."""
        return self.death_year is None

    def is_contemporary(self, year: int) -> bool:
        """Проверяет, был ли автор жив в указанный год."""
        last_year = self.death_year if self.death_year is not None else year
        return self.birth_year <= year <= last_year

    def age_at(self, year: int) -> int:
        """Возвращает возраст автора в указанный год."""
        return max(0, year - self.birth_year)
