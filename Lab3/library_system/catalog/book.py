from __future__ import annotations

from ..constants import (
    BOOK_LOAN_DAYS,
    DEFAULT_LANGUAGE,
    FIELD_ISBN,
    FIELD_PAGES,
    NO_DATA,
    PAGES_PER_HOUR,
    THICK_BOOK_PAGES,
)
from ..validation import require_isbn, require_positive
from .library_item import LibraryItem


class Book(LibraryItem):
    """Печатная книга."""

    def __init__(
        self,
        item_id: str,
        title: str,
        year: int,
        isbn: str,
        pages: int,
        language: str = DEFAULT_LANGUAGE,
        age_limit: int = 0,
    ):
        super().__init__(item_id, title, year, language, age_limit)
        self.isbn = require_isbn(isbn, FIELD_ISBN)
        self.pages = require_positive(pages, FIELD_PAGES)
        self.edition = 1

    def loan_period_days(self) -> int:
        """Книги выдаются на увеличенный срок."""
        return BOOK_LOAN_DAYS

    def reading_time_hours(self) -> float:
        """Оценивает время чтения в часах."""
        return round(self.pages / PAGES_PER_HOUR, 1)

    def is_thick(self) -> bool:
        """Проверяет, что книга объёмная."""
        return self.pages >= THICK_BOOK_PAGES

    def new_edition(self) -> None:
        """Увеличивает номер издания."""
        self.edition += 1

    def citation(self) -> str:
        """Формирует краткое библиографическое описание."""
        publisher_name = self.publisher.name if self.publisher else NO_DATA
        return f"{self.author_names() or NO_DATA}. {self.title}. {publisher_name}, {self.year}."
