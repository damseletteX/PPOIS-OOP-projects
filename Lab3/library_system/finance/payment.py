from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    CURRENCY_DIGITS,
    FIELD_AMOUNT,
    FIELD_ID,
    REASON_ALREADY_REFUNDED,
    REASON_NOT_CASH,
    REASON_TENDER_LOW,
)
from ..enums import PaymentMethod
from ..exceptions import PaymentError
from ..validation import require_positive, require_text

if TYPE_CHECKING:
    from ..people.reader import Reader
    from .fine import Fine


class Payment:
    """Платёж читателя по штрафу."""

    def __init__(
        self,
        payment_id: str,
        reader: Reader,
        fine: Fine,
        amount: float,
        method: PaymentMethod,
        paid_on: date,
    ):
        self.payment_id = require_text(payment_id, FIELD_ID)
        self.reader = reader
        self.fine = fine
        self.amount = require_positive(amount, FIELD_AMOUNT)
        self.method = method
        self.paid_on = paid_on
        self.is_refunded = False

    def process(self) -> None:
        """Проводит платёж и уменьшает остаток штрафа."""
        self.fine.apply_payment(self)

    def refund(self) -> None:
        """Возвращает платёж читателю."""
        if self.is_refunded:
            raise PaymentError(REASON_ALREADY_REFUNDED)
        self.fine.revert_payment(self)
        self.is_refunded = True

    def is_cash(self) -> bool:
        """Проверяет, что платёж внесён наличными."""
        return self.method == PaymentMethod.CASH

    def change_for(self, tendered: float) -> float:
        """Возвращает сдачу с внесённой наличной суммы."""
        if not self.is_cash():
            raise PaymentError(REASON_NOT_CASH)
        if tendered < self.amount:
            raise PaymentError(REASON_TENDER_LOW)
        return round(tendered - self.amount, CURRENCY_DIGITS)
