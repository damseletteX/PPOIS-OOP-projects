from __future__ import annotations

from collections import Counter
from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    CURRENCY_DIGITS,
    FIELD_DATE,
    LABEL_AVERAGE_DAYS,
    LABEL_COLLECTED,
    LABEL_FINES,
    LABEL_LOANS,
    LABEL_OVERDUE,
    LABEL_PERIOD,
    RULE_BEFORE_END,
)
from ..exceptions import ValidationError

if TYPE_CHECKING:
    from ..circulation.loan import Loan
    from ..finance.fine import Fine
    from ..finance.payment import Payment


class LibraryReport:
    """Отчёт о работе библиотеки за период."""

    def __init__(
        self,
        report_id: str,
        period_start: date,
        period_end: date,
        loans: list[Loan],
        fines: list[Fine],
        payments: list[Payment],
    ):
        if period_start > period_end:
            raise ValidationError(FIELD_DATE, RULE_BEFORE_END)
        self.report_id = report_id
        self.period_start = period_start
        self.period_end = period_end
        self.loans = [loan for loan in loans if self._in_period(loan.issued_on)]
        self.fines = [fine for fine in fines if self._in_period(fine.issued_on)]
        self.payments = [pay for pay in payments if self._in_period(pay.paid_on)]

    def overdue_count(self) -> int:
        """Возвращает число выдач с просрочкой на конец периода."""
        return sum(1 for loan in self.loans if loan.days_overdue(self.period_end) > 0)

    def total_fines(self) -> float:
        """Возвращает сумму начисленных штрафов."""
        return round(sum(fine.amount for fine in self.fines), CURRENCY_DIGITS)

    def total_collected(self) -> float:
        """Возвращает сумму фактически полученных платежей."""
        paid = sum(pay.amount for pay in self.payments if not pay.is_refunded)
        return round(paid, CURRENCY_DIGITS)

    def average_loan_days(self) -> float:
        """Возвращает среднюю длительность выдачи."""
        if not self.loans:
            return 0.0
        total_days = sum(loan.days_borrowed(self.period_end) for loan in self.loans)
        return round(total_days / len(self.loans), 1)

    def popular_items(self, limit: int) -> list[tuple[str, int]]:
        """Возвращает самые востребованные издания и число выдач."""
        counter = Counter(loan.copy.item.title for loan in self.loans)
        return counter.most_common(limit)

    def summary(self) -> dict[str, str]:
        """Возвращает основные показатели в виде пар «название — значение»."""
        return {
            LABEL_PERIOD: f"{self.period_start.isoformat()} — {self.period_end.isoformat()}",
            LABEL_LOANS: str(len(self.loans)),
            LABEL_OVERDUE: str(self.overdue_count()),
            LABEL_AVERAGE_DAYS: str(self.average_loan_days()),
            LABEL_FINES: f"{self.total_fines():.2f}",
            LABEL_COLLECTED: f"{self.total_collected():.2f}",
        }

    def _in_period(self, moment: date) -> bool:
        return self.period_start <= moment <= self.period_end
