from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    CURRENCY_DIGITS,
    FIELD_AMOUNT,
    FIELD_ID,
    PERCENT_BASE,
    REASON_OVERPAYMENT,
)
from ..enums import FineReason
from ..exceptions import PaymentError
from ..validation import require_positive, require_text

if TYPE_CHECKING:
    from ..circulation.loan import Loan
    from ..people.reader import Reader
    from .payment import Payment


class Fine:
    """Штраф, начисленный читателю."""

    def __init__(
        self,
        fine_id: str,
        reader: Reader,
        loan: Loan | None,
        amount: float,
        reason: FineReason,
        issued_on: date,
    ):
        self.fine_id = require_text(fine_id, FIELD_ID)
        self.reader = reader
        self.loan = loan
        self.amount = require_positive(amount, FIELD_AMOUNT)
        self.reason = reason
        self.issued_on = issued_on
        self.paid_amount = 0.0
        self.payments: list[Payment] = []

    def balance(self) -> float:
        """Возвращает остаток к оплате."""
        return round(self.amount - self.paid_amount, CURRENCY_DIGITS)

    def is_paid(self) -> bool:
        """Проверяет, что штраф погашен."""
        return self.balance() <= 0

    def paid_percent(self) -> float:
        """Возвращает долю оплаты в процентах."""
        return round(self.paid_amount / self.amount * PERCENT_BASE, CURRENCY_DIGITS)

    def apply_payment(self, payment: Payment) -> None:
        """Засчитывает платёж, не допуская переплаты."""
        if payment.amount > self.balance():
            raise PaymentError(REASON_OVERPAYMENT)
        self.paid_amount += payment.amount
        self.payments.append(payment)

    def revert_payment(self, payment: Payment) -> None:
        """Отменяет ранее засчитанный платёж."""
        if payment in self.payments:
            self.payments.remove(payment)
            self.paid_amount -= payment.amount

    def waive(self) -> None:
        """Списывает остаток штрафа."""
        self.paid_amount = self.amount

    def add_surcharge(self, amount: float) -> None:
        """Увеличивает штраф на сумму."""
        self.amount += require_positive(amount, FIELD_AMOUNT)
