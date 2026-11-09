from datetime import date
from .Expense import Expense


class Budget:
    """Бюджет компании на определённый период и категорию расходов."""

    def __init__(
        self,
        budget_id: str,
        category: str,
        limit_amount: float,
        period_start: date,
        period_end: date,
    ):
        if not budget_id or not category:
            raise ValueError("Не указаны номер бюджета или категория.")
        if limit_amount < 0:
            raise ValueError("Лимит бюджета не может быть отрицательным.")
        if period_end < period_start:
            raise ValueError("Конец периода не может быть раньше его начала.")

        self.budget_id = budget_id
        self.category = category
        self.limit_amount = round(float(limit_amount), 2)
        self.period_start = period_start
        self.period_end = period_end
        self.expenses = []
        self.is_active = True
        self.notes = []

    def add_expense(self, expense: Expense):
        """Добавляет расход, относящийся к бюджету."""
        if not self.is_active:
            raise ValueError("Нельзя добавлять расходы в закрытый бюджет.")
        if expense.category != self.category:
            raise ValueError("Категория расхода не совпадает с бюджетом.")
        if not self.period_start <= expense.expense_date <= self.period_end:
            raise ValueError("Дата расхода находится вне периода бюджета.")
        if expense in self.expenses:
            raise ValueError("Этот расход уже добавлен.")

        self.expenses.append(expense)

    def remove_expense(self, expense_id: str):
        """Удаляет расход из бюджета по его номеру."""
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                self.expenses.remove(expense)
                return True

        return False

    def calculate_spent(self):
        """Считает подтверждённые расходы."""
        total = sum(
            expense.amount
            for expense in self.expenses
            if expense.status in ("approved", "reimbursed")
        )
        return round(total, 2)

    def calculate_remaining(self):
        """Вычисляет оставшуюся сумму бюджета."""
        return round(self.limit_amount - self.calculate_spent(), 2)

    def is_exceeded(self):
        """Проверяет, превышен ли бюджет."""
        return self.calculate_spent() > self.limit_amount

    def get_usage_percentage(self):
        """Вычисляет процент использованного бюджета."""
        if self.limit_amount == 0:
            return 100.0 if self.calculate_spent() > 0 else 0.0

        return round(
            self.calculate_spent() / self.limit_amount * 100,
            2,
        )

    def change_limit(self, new_limit: float):
        """Изменяет установленный лимит бюджета."""
        if not self.is_active:
            raise ValueError("Нельзя изменить закрытый бюджет.")
        if new_limit < 0:
            raise ValueError("Лимит не может быть отрицательным.")

        self.limit_amount = round(float(new_limit), 2)

    def close(self):
        """Закрывает бюджет."""
        if not self.is_active:
            raise ValueError("Бюджет уже закрыт.")

        self.is_active = False

    def reopen(self):
        """Повторно открывает бюджет."""
        if self.is_active:
            raise ValueError("Бюджет уже открыт.")

        self.is_active = True

    def add_note(self, note: str):
        """Добавляет примечание к бюджету."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")
        self.notes.append(note)