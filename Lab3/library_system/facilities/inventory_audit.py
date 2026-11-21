from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import CURRENCY_DIGITS, FIELD_ID, PERCENT_BASE
from ..validation import require_text

if TYPE_CHECKING:
    from ..catalog.item_copy import ItemCopy
    from ..people.staff import Staff
    from .branch import Branch


class InventoryAudit:
    """Инвентаризация фонда филиала."""

    def __init__(self, audit_id: str, branch: Branch, auditor: Staff, audit_date: date):
        self.audit_id = require_text(audit_id, FIELD_ID)
        self.branch = branch
        self.auditor = auditor
        self.audit_date = audit_date
        self.expected_copies: list[ItemCopy] = [
            copy for copy in branch.all_copies() if copy.is_available()
        ]
        self.found_copies: list[ItemCopy] = []

    def register_found(self, copy: ItemCopy) -> None:
        """Отмечает экземпляр найденным на полке."""
        if copy in self.expected_copies and copy not in self.found_copies:
            self.found_copies.append(copy)

    def missing_copies(self) -> list[ItemCopy]:
        """Возвращает экземпляры, которых не оказалось на месте."""
        return [copy for copy in self.expected_copies if copy not in self.found_copies]

    def found_percent(self) -> float:
        """Возвращает долю найденных экземпляров в процентах."""
        if not self.expected_copies:
            return float(PERCENT_BASE)
        share = len(self.found_copies) / len(self.expected_copies)
        return round(share * PERCENT_BASE, CURRENCY_DIGITS)

    def is_complete(self) -> bool:
        """Проверяет, что все экземпляры найдены."""
        return not self.missing_copies()

    def mark_missing_as_lost(self) -> int:
        """Помечает пропавшие экземпляры утерянными и возвращает их число."""
        missing = self.missing_copies()
        for copy in missing:
            copy.mark_lost()
        return len(missing)
