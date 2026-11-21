from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID
from ..validation import require_text

if TYPE_CHECKING:
    from ..people.staff import Staff
    from .loan import Loan


class Renewal:
    """Продление срока возврата."""

    def __init__(self, renewal_id: str, loan: Loan, requested_on: date, new_due_on: date):
        self.renewal_id = require_text(renewal_id, FIELD_ID)
        self.loan = loan
        self.requested_on = requested_on
        self.previous_due_on = loan.due_on
        self.new_due_on = new_due_on
        self.approved_by: Staff | None = None

    def extra_days(self) -> int:
        """Возвращает, на сколько дней продлён срок."""
        return (self.new_due_on - self.previous_due_on).days

    def approve(self, staff: Staff) -> None:
        """Фиксирует сотрудника, одобрившего продление."""
        self.approved_by = staff

    def is_approved(self) -> bool:
        """Проверяет, что продление одобрено."""
        return self.approved_by is not None
