from datetime import date
from .payment import Payment
from ..exceptions import (
    PaymentError,
)


class Invoice:
    """Счёт, выставленный клиенту за транспортный заказ."""

    def __init__(
        self,
        invoice_id: str,
        order,
        due_date: date,
        tax_rate: float = 0.0,
        discount_amount: float = 0.0,
    ):
        if not invoice_id:
            raise ValueError("Не указан номер счёта.")
        if not 0 <= tax_rate <= 1:
            raise ValueError("Налоговая ставка должна быть от 0 до 1.")
        if discount_amount < 0:
            raise ValueError("Скидка не может быть отрицательной.")

        self.invoice_id = invoice_id
        self.order = order
        self.issue_date = date.today()
        self.due_date = due_date
        self.tax_rate = tax_rate
        self.discount_amount = round(float(discount_amount), 2)

        # Сохраняем данные позиций на момент создания счёта.
        self.items = []
        for item in order.items:
            self.items.append(
                {
                    "item_id": item.item_id,
                    "description": item.cargo.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                }
            )

        self.additional_charges = []
        self.payments = []
        self.amount_paid = 0.0
        self.status = "draft"
        self.notes = []

    def calculate_subtotal(self):
        """Вычисляет стоимость всех позиций счёта."""
        return round(
            sum(item["quantity"] * item["unit_price"] for item in self.items),
            2,
        )

    def calculate_tax(self):
        """Вычисляет налог с учётом скидки и дополнительных расходов."""
        taxable_amount = (
            self.calculate_subtotal()
            + sum(charge["amount"] for charge in self.additional_charges)
            - self.discount_amount
        )
        return round(max(0, taxable_amount) * self.tax_rate, 2)

    def calculate_total(self):
        """Вычисляет окончательную сумму счёта."""
        subtotal = self.calculate_subtotal()
        charges = sum(charge["amount"] for charge in self.additional_charges)
        taxable_amount = max(
            0,
            subtotal + charges - self.discount_amount,
        )
        return round(taxable_amount + self.calculate_tax(), 2)

    def add_charge(self, description: str, amount: float):
        """Добавляет дополнительную услугу или сбор."""
        if self.status != "draft":
            raise PaymentError("Изменять можно только черновик счёта.")
        if not description or amount < 0:
            raise ValueError("Некорректное описание или сумма сбора.")

        self.additional_charges.append(
            {
                "description": description,
                "amount": round(float(amount), 2),
            }
        )

    def apply_discount(self, amount: float):
        """Устанавливает скидку на счёт."""
        if self.status != "draft":
            raise PaymentError("Скидку можно изменить только в черновике.")
        if amount < 0:
            raise ValueError("Скидка не может быть отрицательной.")
        if amount > self.calculate_subtotal():
            raise ValueError("Скидка превышает стоимость позиций.")

        self.discount_amount = round(float(amount), 2)

    def issue(self):
        """Выставляет счёт клиенту."""
        if self.status != "draft":
            raise PaymentError("Счёт уже был выставлен или закрыт.")
        if self.due_date < self.issue_date:
            raise ValueError("Срок оплаты не может быть раньше даты счёта.")

        self.status = "issued"

    def can_accept_payment(self, amount: float):
        """Проверяет, можно ли принять указанную сумму."""
        if self.status not in ("issued", "partially_paid"):
            return False
        return amount > 0 and amount <= self.get_balance_due()

    def register_payment(self, payment: Payment):
        """Регистрирует успешно проведённую оплату."""
        if payment.invoice is not self:
            raise PaymentError("Оплата относится к другому счёту.")
        if payment.status not in (
            "completed",
            "partially_refunded",
            "refunded",
        ):
            raise PaymentError("Нельзя зарегистрировать неуспешную оплату.")
        if payment in self.payments:
            raise PaymentError("Эта оплата уже зарегистрирована.")
        if payment.amount > self.get_balance_due():
            raise PaymentError("Сумма оплаты превышает остаток по счёту.")

        self.payments.append(payment)
        self.amount_paid = round(self.amount_paid + payment.amount, 2)

        if self.amount_paid >= self.calculate_total():
            self.status = "paid"
        else:
            self.status = "partially_paid"

    def register_refund(self, amount: float):
        """Учитывает возврат ранее полученных денежных средств."""
        if amount <= 0 or amount > self.amount_paid:
            raise PaymentError("Некорректная сумма возврата.")

        self.amount_paid = round(self.amount_paid - amount, 2)

        if self.amount_paid == 0:
            self.status = "issued"
        else:
            self.status = "partially_paid"

    def get_balance_due(self):
        """Возвращает оставшуюся сумму к оплате."""
        return round(max(0, self.calculate_total() - self.amount_paid), 2)

    def is_overdue(self, check_date: date | None = None):
        """Проверяет, истёк ли срок оплаты."""
        check_date = check_date or date.today()
        return self.status in ("issued", "partially_paid") and check_date > self.due_date

    def update_due_date(self, new_date: date):
        """Изменяет срок оплаты."""
        if self.status in ("paid", "cancelled"):
            raise PaymentError("Нельзя изменить срок закрытого счёта.")
        if new_date < self.issue_date:
            raise ValueError("Новая дата не может быть раньше даты счёта.")

        self.due_date = new_date

    def cancel(self):
        """Отменяет счёт, если по нему ещё не было оплат."""
        if self.status not in ("draft", "issued"):
            raise PaymentError("Этот счёт нельзя отменить.")
        if self.amount_paid > 0:
            raise PaymentError("Нельзя отменить оплаченный счёт.")

        self.status = "cancelled"

    def add_note(self, note: str):
        """Добавляет примечание к счёту."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")
        self.notes.append(note)