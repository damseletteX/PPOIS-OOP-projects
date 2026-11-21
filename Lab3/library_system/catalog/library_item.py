from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import (
    DEFAULT_LANGUAGE,
    FIELD_AGE,
    FIELD_ID,
    FIELD_NAME,
    FIELD_TITLE,
    FIELD_YEAR,
    ITEM_LOAN_DAYS,
    RECENT_ITEM_YEARS,
    TEXT_JOINER,
)
from ..validation import require_non_negative, require_positive, require_text

if TYPE_CHECKING:
    from .author import Author
    from .category import Category
    from .item_copy import ItemCopy
    from .publisher import Publisher
    from .review import Review


class LibraryItem:
    """Базовое издание каталога."""

    def __init__(
        self,
        item_id: str,
        title: str,
        year: int,
        language: str = DEFAULT_LANGUAGE,
        age_limit: int = 0,
    ):
        self.item_id = require_text(item_id, FIELD_ID)
        self.title = require_text(title, FIELD_TITLE)
        self.year = require_positive(year, FIELD_YEAR)
        self.language = require_text(language, FIELD_NAME)
        self.age_limit = require_non_negative(age_limit, FIELD_AGE)
        self.category: Category | None = None
        self.publisher: Publisher | None = None
        self.authors: list[Author] = []
        self.copies: list[ItemCopy] = []
        self.reviews: list[Review] = []

    def add_author(self, author: Author) -> None:
        """Добавляет автора и регистрирует издание в его работах."""
        if author not in self.authors:
            self.authors.append(author)
            author.add_work(self)

    def author_names(self) -> str:
        """Возвращает имена авторов через запятую."""
        return TEXT_JOINER.join(author.name for author in self.authors)

    def set_publisher(self, publisher: Publisher) -> None:
        """Назначает издательство."""
        self.publisher = publisher
        publisher.publish(self)

    def assign_category(self, category: Category) -> None:
        """Относит издание к рубрике."""
        self.category = category
        category.add_item(self)

    def add_copy(self, copy: ItemCopy) -> None:
        """Добавляет физический экземпляр издания."""
        if copy not in self.copies:
            self.copies.append(copy)

    def available_copies(self) -> list[ItemCopy]:
        """Возвращает экземпляры, которые можно выдать."""
        return [copy for copy in self.copies if copy.is_available()]

    def has_available_copy(self) -> bool:
        """Проверяет, есть ли свободный экземпляр."""
        return bool(self.available_copies())

    def copies_count(self) -> int:
        """Возвращает общее число экземпляров."""
        return len(self.copies)

    def add_review(self, review: Review) -> None:
        """Добавляет отзыв читателя."""
        self.reviews.append(review)

    def average_rating(self) -> float:
        """Возвращает среднюю оценку по одобренным отзывам."""
        ratings = [review.rating for review in self.reviews if review.is_approved]
        return round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    def loan_period_days(self) -> int:
        """Возвращает базовый срок выдачи."""
        return ITEM_LOAN_DAYS

    def is_loanable(self) -> bool:
        """Проверяет, можно ли выдавать издание на руки."""
        return True

    def is_suitable_for_age(self, age: int) -> bool:
        """Проверяет возрастное ограничение."""
        return age >= self.age_limit

    def is_recent(self, current_year: int) -> bool:
        """Проверяет, что издание вышло недавно."""
        return current_year - self.year <= RECENT_ITEM_YEARS
