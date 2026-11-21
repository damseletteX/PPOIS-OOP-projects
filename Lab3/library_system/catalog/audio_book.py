from __future__ import annotations

from math import ceil

from ..constants import (
    AUDIO_DISC_MINUTES,
    AUDIO_LONG_MINUTES,
    AUDIOBOOK_LOAN_DAYS,
    DEFAULT_LANGUAGE,
    FIELD_DURATION,
    FIELD_NAME,
    MINUTES_IN_HOUR,
)
from ..validation import require_positive, require_text
from .library_item import LibraryItem


class AudioBook(LibraryItem):
    """Аудиокнига на дисках."""

    def __init__(
        self,
        item_id: str,
        title: str,
        year: int,
        narrator: str,
        duration_minutes: int,
        language: str = DEFAULT_LANGUAGE,
        age_limit: int = 0,
    ):
        super().__init__(item_id, title, year, language, age_limit)
        self.narrator = require_text(narrator, FIELD_NAME)
        self.duration_minutes = require_positive(duration_minutes, FIELD_DURATION)

    def loan_period_days(self) -> int:
        """Срок выдачи аудиокниги."""
        return AUDIOBOOK_LOAN_DAYS

    def duration_hours(self) -> float:
        """Возвращает длительность в часах."""
        return round(self.duration_minutes / MINUTES_IN_HOUR, 1)

    def discs_needed(self) -> int:
        """Возвращает число дисков, необходимых для записи."""
        return ceil(self.duration_minutes / AUDIO_DISC_MINUTES)

    def is_long(self) -> bool:
        """Проверяет, что запись длинная."""
        return self.duration_minutes >= AUDIO_LONG_MINUTES
