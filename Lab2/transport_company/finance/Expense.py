from datetime import date


class Expense:
    """Расход транспортной компании."""

    def __init__(
        self,
        expense_id: str,
        category: str,
        description: str,
        amount: float,
        expense_date: date | None = None,
        receipt_number: str = "",
    ):
        if not expense_id:
            raise ValueError("Не указан номер расхода.")
        if not category or not description:
            raise ValueError("Категория и описание обязательны.")
        if amount <= 0:
            raise ValueError("Сумма расхода должна быть положительной.")

        self.expense_id = expense_id
        self.category = category
        self.description = description
        self.amount = round(float(amount), 2)
        self.expense_date = expense_date or date.today()
        self.receipt_number = receipt_number
        self.status = "pending"
        self.approved_by = None
        self.rejection_reason = ""
        self.is_reimbursed = False
        self.notes = []

    def approve(self, manager):
        """Подтверждает расход руководителем."""
        if self.status != "pending":
            raise ValueError("Можно подтвердить только ожидающий расход.")
        if manager is None:
            raise ValueError("Не указан руководитель.")

        self.approved_by = manager
        self.status = "approved"

    def reject(self, reason: str):
        """Отклоняет расход."""
        if self.status != "pending":
            raise ValueError("Можно отклонить только ожидающий расход.")

        self.rejection_reason = reason
        self.status = "rejected"

    def mark_reimbursed(self):
        """Отмечает расход как возмещённый."""
        if self.status != "approved":
            raise ValueError("Возместить можно только подтверждённый расход.")

        self.is_reimbursed = True
        self.status = "reimbursed"

    def update_amount(self, new_amount: float):
        """Изменяет сумму расхода до его подтверждения."""
        if self.status != "pending":
            raise ValueError("Нельзя изменить подтверждённый расход.")
        if new_amount <= 0:
            raise ValueError("Сумма должна быть положительной.")

        self.amount = round(float(new_amount), 2)

    def change_category(self, new_category: str):
        """Изменяет категорию расхода."""
        if self.status != "pending":
            raise ValueError("Категорию можно изменить только до подтверждения.")
        if not new_category:
            raise ValueError("Категория не может быть пустой.")

        self.category = new_category

    def add_note(self, note: str):
        """Добавляет комментарий к расходу."""
        if not note:
            raise ValueError("Комментарий не может быть пустым.")
        self.notes.append(note)

    def has_receipt(self):
        """Проверяет наличие номера подтверждающего документа."""
        return bool(self.receipt_number)