from datetime import date
from .Transaction import Transaction
from ..exceptions import (
    PaymentError,
)


class Payment:
    """Оплата транспортного заказа."""

    def __init__(
        self,
        payment_id: str,
        order,
        amount: float,
        payment_method: str,
        invoice=None,
        payment_date: date | None = None,
        reference: str = "",
    ):
        if not payment_id:
            raise ValueError("Не указан номер оплаты.")
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной.")
        if not payment_method:
            raise ValueError("Не указан способ оплаты.")

        self.payment_id = payment_id
        self.order = order
        self.invoice = invoice
        self.amount = round(float(amount), 2)
        self.payment_method = payment_method
        self.payment_date = payment_date or date.today()
        self.reference = reference
        self.status = "pending"
        self.transaction_id = None
        self.refunded_amount = 0.0
        self.transactions = []
        self.notes = []

    def process(self):
        """Обрабатывает оплату и создаёт транзакцию."""
        if self.status != "pending":
            raise PaymentError("Эту оплату нельзя обработать повторно.")

        if self.invoice and not self.invoice.can_accept_payment(self.amount):
            raise PaymentError("Сумма превышает остаток по счёту.")

        transaction = Transaction(
            transaction_id=f"{self.payment_id}-TXN-1",
            payment=self,
            transaction_type="payment",
            amount=self.amount,
            description="Оплата транспортного заказа",
        )
        transaction.mark_successful()

        self.transactions.append(transaction)
        self.transaction_id = transaction.transaction_id
        self.status = "completed"

        if self.invoice:
            self.invoice.register_payment(self)

        return transaction

    def fail(self, reason: str):
        """Отмечает оплату как неуспешную."""
        if self.status != "pending":
            raise PaymentError("Можно отменить только ожидающую оплату.")

        self.status = "failed"
        self.add_note(f"Причина отказа: {reason}")

    def refund(self, amount: float | None = None):
        """Возвращает всю сумму или её часть."""
        if self.status not in ("completed", "partially_refunded"):
            raise PaymentError("Возврат невозможен для этой оплаты.")

        if amount is None:
            amount = self.amount - self.refunded_amount

        if amount <= 0:
            raise PaymentError("Сумма возврата должна быть положительной.")

        if amount > self.amount - self.refunded_amount:
            raise PaymentError("Сумма возврата превышает доступный остаток.")

        refund_transaction = Transaction(
            transaction_id=f"{self.payment_id}-REFUND-{len(self.transactions)}",
            payment=self,
            transaction_type="refund",
            amount=amount,
            description="Возврат денежных средств",
        )
        refund_transaction.mark_successful()

        self.transactions.append(refund_transaction)
        self.refunded_amount = round(self.refunded_amount + amount, 2)

        if self.refunded_amount == self.amount:
            self.status = "refunded"
        else:
            self.status = "partially_refunded"

        if self.invoice:
            self.invoice.register_refund(amount)

        return refund_transaction

    def remaining_refundable_amount(self):
        """Возвращает сумму, которую ещё можно вернуть."""
        return round(self.amount - self.refunded_amount, 2)

    def change_payment_method(self, new_method: str):
        """Изменяет способ оплаты до её обработки."""
        if self.status != "pending":
            raise PaymentError("Способ оплаты уже нельзя изменить.")
        if not new_method:
            raise ValueError("Не указан новый способ оплаты.")

        self.payment_method = new_method

    def add_note(self, note: str):
        """Добавляет комментарий к оплате."""
        if not note:
            raise ValueError("Комментарий не может быть пустым.")
        self.notes.append(note)

    def is_successful(self):
        """Проверяет, прошла ли оплата успешно."""
        return self.status in ("completed", "partially_refunded", "refunded")