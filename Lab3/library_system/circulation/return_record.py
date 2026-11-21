from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID
from ..enums import CopyCondition
from ..validation import require_text

if TYPE_CHECKING:
    from ..people.librarian import Librarian
    from .loan import Loan


class ReturnRecord:
    """Запись о возврате издания."""

    def __init__(
        self,
        record_id: str,
        loan: Loan,
        returned_on: date,
        condition: CopyCondition,
        received_by: Librarian,
    ):
        self.record_id = require_text(record_id, FIELD_ID)
        self.loan = loan
        self.returned_on = returned_on
        self.condition = condition
        self.received_by = received_by
        self.notes: list[str] = []

    def is_damaged(self) -> bool:
        """Проверяет, что издание возвращено повреждённым."""
        return self.condition == CopyCondition.DAMAGED

    def was_late(self) -> bool:
        """Проверяет, что издание возвращено после срока."""
        return self.returned_on > self.loan.due_on

    def days_late(self) -> int:
        """Возвращает число дней просрочки."""
        return max(0, (self.returned_on - self.loan.due_on).days)

    def add_note(self, text: str) -> None:
        """Добавляет заметку о состоянии издания."""
        self.notes.append(text.strip())

    def requires_repair(self) -> bool:
        """Проверяет, нужно ли отправить экземпляр в ремонт."""
        return self.is_damaged() and self.loan.copy.needs_repair()
