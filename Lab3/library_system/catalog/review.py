from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    FIELD_ID,
    FIELD_RATING,
    MAX_RATING,
    MIN_RATING,
    POSITIVE_RATING_MIN,
    RECENT_REVIEW_DAYS,
)
from ..validation import require_in_range, require_text

if TYPE_CHECKING:
    from ..people.reader import Reader
    from .library_item import LibraryItem


class Review:
    """Отзыв читателя об издании."""

    def __init__(
        self,
        review_id: str,
        item: LibraryItem,
        reader: Reader,
        rating: int,
        text: str,
        created_on: date,
    ):
        self.review_id = require_text(review_id, FIELD_ID)
        self.item = item
        self.reader = reader
        self.rating = require_in_range(rating, MIN_RATING, MAX_RATING, FIELD_RATING)
        self.text = text.strip()
        self.created_on = created_on
        self.is_approved = False

    def approve(self) -> None:
        """Одобряет отзыв к публикации."""
        self.is_approved = True

    def edit(self, text: str, rating: int) -> None:
        """Изменяет текст и оценку, повторно отправляя отзыв на проверку."""
        self.rating = require_in_range(rating, MIN_RATING, MAX_RATING, FIELD_RATING)
        self.text = text.strip()
        self.is_approved = False

    def is_positive(self) -> bool:
        """Проверяет, что оценка высокая."""
        return self.rating >= POSITIVE_RATING_MIN

    def is_recent(self, on_date: date) -> bool:
        """Проверяет, что отзыв написан недавно."""
        return (on_date - self.created_on).days <= RECENT_REVIEW_DAYS
