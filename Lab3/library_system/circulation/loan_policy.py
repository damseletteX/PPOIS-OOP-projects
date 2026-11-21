from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import (
    MAX_LOANS_HARD_CAP,
    MAX_RENEWALS,
    MAX_UNPAID_FINE,
    RENEWAL_DAYS,
)

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem
    from ..people.reader import Reader
    from .loan import Loan


class LoanPolicy:
    """Правила выдачи и продления изданий."""

    def __init__(
        self,
        hard_loan_cap: int = MAX_LOANS_HARD_CAP,
        max_renewals: int = MAX_RENEWALS,
        renewal_days: int = RENEWAL_DAYS,
        max_unpaid_fine: float = MAX_UNPAID_FINE,
    ):
        self.hard_loan_cap = hard_loan_cap
        self.max_renewals = max_renewals
        self.renewal_days = renewal_days
        self.max_unpaid_fine = max_unpaid_fine

    def effective_loan_limit(self, reader: Reader) -> int:
        """Возвращает лимит выдач читателя с учётом общего потолка."""
        return min(reader.loan_limit(), self.hard_loan_cap)

    def loan_period_for(self, reader: Reader, item: LibraryItem) -> int:
        """Возвращает срок выдачи в днях для пары читатель — издание."""
        return item.loan_period_days() + reader.loan_bonus_days()

    def due_date_for(self, reader: Reader, item: LibraryItem, on_date: date) -> date:
        """Возвращает срок возврата при выдаче в указанный день."""
        return on_date + timedelta(days=self.loan_period_for(reader, item))

    def renewals_left(self, loan: Loan) -> int:
        """Возвращает число оставшихся продлений."""
        return max(0, self.max_renewals - loan.renewals_count())

    def can_renew(self, loan: Loan) -> bool:
        """Проверяет, не исчерпан ли лимит продлений."""
        return self.renewals_left(loan) > 0

    def blocks_borrowing(self, unpaid_total: float) -> bool:
        """Проверяет, мешают ли штрафы новой выдаче."""
        return unpaid_total > self.max_unpaid_fine
