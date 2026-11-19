from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..exceptions import (
    PaymentError,
)

if TYPE_CHECKING:
    from .payment import Payment


class Transaction:
    """Финансовая транзакция, связанная с оплатой."""

    def __init__(
        self,
        transaction_id: str,
        payment: Payment,
        transaction_type: str,
        amount: float,
        description: str = "",
    ):
        if not transaction_id:
            raise ValueError("Не указан номер транзакции.")
        if transaction_type not in ("payment", "refund"):
            raise ValueError("Неизвестный тип транзакции.")
        if amount <= 0:
            raise ValueError("Сумма транзакции должна быть положительной.")

        self.transaction_id = transaction_id
        self.payment = payment
        self.transaction_type = transaction_type
        self.amount = round(float(amount), 2)
        self.timestamp = datetime.now()
        self.description = description
        self.status = "pending"
        self.external_reference = ""
        self.failure_reason = ""

    def mark_successful(self):
        """Подтверждает успешное выполнение транзакции."""
        if self.status != "pending":
            raise PaymentError("Транзакция уже обработана.")

        self.status = "successful"

    def mark_failed(self, reason: str):
        """Отмечает транзакцию как неуспешную."""
        if self.status != "pending":
            raise PaymentError("Нельзя изменить обработанную транзакцию.")

        self.status = "failed"
        self.failure_reason = reason

    def reverse(self, reason: str):
        """Помечает успешную транзакцию как отменённую."""
        if self.status != "successful":
            raise PaymentError("Отменить можно только успешную транзакцию.")

        self.status = "reversed"
        self.description += f". Причина отмены: {reason}"

    def set_external_reference(self, reference: str):
        """Сохраняет внешний номер операции."""
        if not reference:
            raise ValueError("Внешний номер не может быть пустым.")

        self.external_reference = reference

    def is_refund(self):
        """Проверяет, является ли транзакция возвратом."""
        return self.transaction_type == "refund"