from __future__ import annotations

from ..constants import (
    DEFAULT_LANGUAGE,
    FIELD_CODE,
    FIELD_ID,
    MAGAZINE_LOAN_DAYS,
)
from ..validation import require_positive, require_text
from .library_item import LibraryItem


class Magazine(LibraryItem):
    """Номер периодического издания."""

    def __init__(
        self,
        item_id: str,
        title: str,
        year: int,
        issn: str,
        issue_number: int,
        language: str = DEFAULT_LANGUAGE,
        age_limit: int = 0,
    ):
        super().__init__(item_id, title, year, language, age_limit)
        self.issn = require_text(issn, FIELD_CODE)
        self.issue_number = require_positive(issue_number, FIELD_ID)
        self.is_latest_issue = True

    def loan_period_days(self) -> int:
        """Журналы выдаются на короткий срок."""
        return MAGAZINE_LOAN_DAYS

    def is_loanable(self) -> bool:
        """Свежий номер выдаётся только в читальном зале."""
        return not self.is_latest_issue

    def archive(self) -> None:
        """Переводит номер в архив: его можно брать на руки."""
        self.is_latest_issue = False

    def next_issue_number(self) -> int:
        """Возвращает номер следующего выпуска."""
        return self.issue_number + 1

    def issue_label(self) -> str:
        """Возвращает подпись выпуска вида «№5/2026»."""
        return f"№{self.issue_number}/{self.year}"
