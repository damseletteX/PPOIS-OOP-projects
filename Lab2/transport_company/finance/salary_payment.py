from datetime import date
from ..exceptions import (
    PaymentError,
)


class SalaryPayment:
    """Начисление и выплата заработной платы сотруднику."""

    def __init__(
        self,
        salary_payment_id: str,
        employee,
        period_start: date,
        period_end: date,
        base_salary: float,
    ):
        if not salary_payment_id:
            raise ValueError("Не указан номер выплаты.")
        if period_end < period_start:
            raise ValueError("Некорректный период начисления.")
        if base_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")

        self.salary_payment_id = salary_payment_id
        self.employee = employee
        self.period_start = period_start
        self.period_end = period_end
        self.base_salary = round(float(base_salary), 2)
        self.bonus = 0.0
        self.deductions = 0.0
        self.status = "pending"
        self.payment_date = None
        self.notes = []

    def calculate_net_amount(self):
        """Вычисляет итоговую сумму зарплаты."""
        return round(
            self.base_salary + self.bonus - self.deductions,
            2,
        )

    def add_bonus(self, amount: float):
        """Добавляет премию сотруднику."""
        if self.status != "pending":
            raise ValueError("Нельзя изменить уже выплаченную зарплату.")
        if amount <= 0:
            raise ValueError("Премия должна быть положительной.")

        self.bonus = round(self.bonus + amount, 2)

    def add_deduction(self, amount: float):
        """Добавляет удержание из зарплаты."""
        if self.status != "pending":
            raise ValueError("Нельзя изменить уже выплаченную зарплату.")
        if amount <= 0:
            raise ValueError("Удержание должно быть положительным.")
        if amount > self.base_salary + self.bonus - self.deductions:
            raise ValueError("Удержание превышает начисленную сумму.")

        self.deductions = round(self.deductions + amount, 2)

    def pay(self, payment_date: date | None = None):
        """Подтверждает выплату заработной платы."""
        if self.status != "pending":
            raise PaymentError("Эта зарплата уже обработана.")
        if self.calculate_net_amount() < 0:
            raise PaymentError("Итоговая зарплата не может быть отрицательной.")

        self.payment_date = payment_date or date.today()
        self.status = "paid"

    def cancel(self):
        """Отменяет начисление до выплаты."""
        if self.status != "pending":
            raise PaymentError("Нельзя отменить уже выплаченную зарплату.")

        self.status = "cancelled"

    def is_paid(self):
        """Проверяет, была ли выплачена зарплата."""
        return self.status == "paid"

    def add_note(self, note: str):
        """Добавляет комментарий к начислению."""
        if not note:
            raise ValueError("Комментарий не может быть пустым.")
        self.notes.append(note)