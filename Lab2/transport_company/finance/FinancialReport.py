from datetime import date, datetime
from .Payment import Payment
from .Expense import Expense
from .SalaryPayment import SalaryPayment


class FinancialReport:
    """Финансовый отчёт компании за выбранный период."""

    def __init__(
        self,
        report_id: str,
        period_start: date,
        period_end: date,
    ):
        if not report_id:
            raise ValueError("Не указан номер отчёта.")
        if period_end < period_start:
            raise ValueError("Некорректный период отчёта.")

        self.report_id = report_id
        self.period_start = period_start
        self.period_end = period_end
        self.payments = []
        self.expenses = []
        self.salary_payments = []
        self.created_at = datetime.now()
        self.is_finalized = False
        self.notes = []

    @staticmethod
    def _to_date(value):
        """Преобразует дату или дату со временем в объект date."""
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return None

    def _is_in_period(self, value):
        """Проверяет, входит ли дата в период отчёта."""
        record_date = self._to_date(value)

        return record_date is not None and self.period_start <= record_date <= self.period_end

    def add_payment(self, payment: Payment):
        """Добавляет оплату, совершённую в период отчёта."""
        if self.is_finalized:
            raise ValueError("Нельзя изменять завершённый отчёт.")
        if not self._is_in_period(payment.payment_date):
            raise ValueError("Оплата находится вне периода отчёта.")
        if payment in self.payments:
            raise ValueError("Оплата уже добавлена в отчёт.")

        self.payments.append(payment)

    def add_expense(self, expense: Expense):
        """Добавляет расход, совершённый в период отчёта."""
        if self.is_finalized:
            raise ValueError("Нельзя изменять завершённый отчёт.")
        if not self._is_in_period(expense.expense_date):
            raise ValueError("Расход находится вне периода отчёта.")
        if expense in self.expenses:
            raise ValueError("Расход уже добавлен в отчёт.")

        self.expenses.append(expense)

    def add_salary_payment(self, salary_payment: SalaryPayment):
        """Добавляет выплату зарплаты в отчёт."""
        if self.is_finalized:
            raise ValueError("Нельзя изменять завершённый отчёт.")
        if salary_payment.status != "paid":
            raise ValueError("В отчёт добавляются только выплаченные зарплаты.")
        if not self._is_in_period(salary_payment.payment_date):
            raise ValueError("Выплата находится вне периода отчёта.")
        if salary_payment in self.salary_payments:
            raise ValueError("Выплата уже добавлена в отчёт.")

        self.salary_payments.append(salary_payment)

    def calculate_revenue(self):
        """Считает поступления от успешно обработанных оплат."""
        total = sum(
            payment.amount - payment.refunded_amount
            for payment in self.payments
            if payment.status
            in (
                "completed",
                "partially_refunded",
                "refunded",
            )
        )
        return round(total, 2)

    def calculate_expenses(self):
        """Считает подтверждённые расходы компании."""
        total = sum(
            expense.amount
            for expense in self.expenses
            if expense.status in ("approved", "reimbursed")
        )
        return round(total, 2)

    def calculate_salary_costs(self):
        """Считает расходы компании на выплаченную зарплату."""
        total = sum(
            payment.calculate_net_amount()
            for payment in self.salary_payments
            if payment.status == "paid"
        )
        return round(total, 2)

    def calculate_total_costs(self):
        """Считает все расходы, включая зарплаты."""
        return round(
            self.calculate_expenses() + self.calculate_salary_costs(),
            2,
        )

    def calculate_profit(self):
        """Вычисляет разницу между доходами и расходами."""
        return round(
            self.calculate_revenue() - self.calculate_total_costs(),
            2,
        )

    def get_payment_count(self):
        """Возвращает количество успешных оплат."""
        return sum(
            1
            for payment in self.payments
            if payment.status
            in (
                "completed",
                "partially_refunded",
                "refunded",
            )
        )

    def finalize(self):
        """Завершает формирование отчёта."""
        if self.is_finalized:
            raise ValueError("Отчёт уже завершён.")

        self.is_finalized = True

    def add_note(self, note: str):
        """Добавляет примечание к отчёту."""
        if self.is_finalized:
            raise ValueError("Нельзя изменять завершённый отчёт.")
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)

    def generate_summary(self):
        """Формирует сводные финансовые показатели."""
        return {
            "report_id": self.report_id,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "revenue": self.calculate_revenue(),
            "expenses": self.calculate_expenses(),
            "salary_costs": self.calculate_salary_costs(),
            "total_costs": self.calculate_total_costs(),
            "profit": self.calculate_profit(),
            "payment_count": self.get_payment_count(),
            "is_finalized": self.is_finalized,
        }