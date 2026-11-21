from __future__ import annotations

from ..constants import DEFAULT_LANGUAGE, FIELD_NAME
from ..enums import DegreeLevel
from ..validation import require_text
from .library_item import LibraryItem


class Thesis(LibraryItem):
    """Диссертация или дипломная работа (читается только в зале)."""

    def __init__(
        self,
        item_id: str,
        title: str,
        year: int,
        supervisor: str,
        university: str,
        degree: DegreeLevel,
        language: str = DEFAULT_LANGUAGE,
    ):
        super().__init__(item_id, title, year, language)
        self.supervisor = require_text(supervisor, FIELD_NAME)
        self.university = require_text(university, FIELD_NAME)
        self.degree = degree

    def is_loanable(self) -> bool:
        """Диссертации на руки не выдаются."""
        return False

    def is_doctoral(self) -> bool:
        """Проверяет, что это докторская диссертация."""
        return self.degree == DegreeLevel.DOCTORAL

    def supervised_by(self, name: str) -> bool:
        """Проверяет, что работой руководил указанный человек."""
        return self.supervisor.lower() == name.strip().lower()
