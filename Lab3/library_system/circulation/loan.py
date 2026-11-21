from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import ENTITY_LOAN, FIELD_ID
from ..enums import LoanStatus
from ..validation import ensure_transition, require_text

if TYPE_CHECKING:
    from ..catalog.item_copy import ItemCopy
    from ..people.librarian import Librarian
    from ..people.reader import Reader
    from .renewal import Renewal


class Loan:
    """Выдача экземпляра читателю."""

    def __init__(
        self,
        loan_id: str,
        reader: Reader,
        copy: ItemCopy,
        librarian: Librarian,
        issued_on: date,
        due_on: date,
    ):
        self.loan_id = require_text(loan_id, FIELD_ID)
        self.reader = reader
        self.copy = copy
        self.librarian = librarian
        self.issued_on = issued_on
        self.due_on = due_on
        self.returned_on: date | None = None
        self.renewals: list[Renewal] = []
        self.status = LoanStatus.ACTIVE

    def is_active(self) -> bool:
        """Проверяет, что издание ещё на руках."""
        return self.status == LoanStatus.ACTIVE

    def is_overdue(self, on_date: date) -> bool:
        """Проверяет, что срок возврата прошёл."""
        return self.is_active() and on_date > self.due_on

    def days_overdue(self, on_date: date) -> int:
        """Возвращает число дней просрочки на дату (или на дату возврата)."""
        end_date = self.returned_on or on_date
        return max(0, (end_date - self.due_on).days)

    def days_borrowed(self, on_date: date) -> int:
        """Возвращает, сколько дней издание находилось на руках."""
        end_date = self.returned_on or on_date
        return (end_date - self.issued_on).days

    def renewals_count(self) -> int:
        """Возвращает число продлений."""
        return len(self.renewals)

    def close(self, on_date: date) -> None:
        """Закрывает выдачу при возврате."""
        ensure_transition(ENTITY_LOAN, self.status, {LoanStatus.ACTIVE}, LoanStatus.RETURNED)
        self.status = LoanStatus.RETURNED
        self.returned_on = on_date

    def extend(self, renewal: Renewal) -> None:
        """Применяет продление к выдаче."""
        ensure_transition(ENTITY_LOAN, self.status, {LoanStatus.ACTIVE}, LoanStatus.ACTIVE)
        self.due_on = renewal.new_due_on
        self.renewals.append(renewal)

    def mark_lost(self) -> None:
        """Отмечает издание утерянным."""
        ensure_transition(ENTITY_LOAN, self.status, {LoanStatus.ACTIVE}, LoanStatus.LOST)
        self.status = LoanStatus.LOST
