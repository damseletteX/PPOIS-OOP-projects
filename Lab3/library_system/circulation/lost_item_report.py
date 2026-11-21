from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID
from ..validation import require_text

if TYPE_CHECKING:
    from ..finance.fine import Fine
    from .loan import Loan


class LostItemReport:
    """Акт об утрате издания читателем."""

    def __init__(self, report_id: str, loan: Loan, reported_on: date, fine: Fine):
        self.report_id = require_text(report_id, FIELD_ID)
        self.loan = loan
        self.reported_on = reported_on
        self.fine = fine

    def compensation_due(self) -> float:
        """Возвращает неоплаченную часть компенсации."""
        return self.fine.balance()

    def is_compensated(self) -> bool:
        """Проверяет, что компенсация выплачена полностью."""
        return self.fine.is_paid()

    def days_since_report(self, on_date: date) -> int:
        """Возвращает число дней с момента составления акта."""
        return (on_date - self.reported_on).days

    def description(self) -> str:
        """Возвращает краткое описание утраты."""
        return f"{self.loan.copy.item.title} ({self.loan.copy.inventory_number})"
