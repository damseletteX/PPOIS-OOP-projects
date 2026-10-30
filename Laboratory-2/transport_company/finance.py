
"""Финансовый модуль транспортной компании."""

from datetime import date, datetime

from exceptions import PaymentError


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
            self.items.append({
                "item_id": item.item_id,
                "description": item.cargo.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            })

        self.additional_charges = []
        self.payments = []
        self.amount_paid = 0.0
        self.status = "draft"
        self.notes = []

    def calculate_subtotal(self):
        """Вычисляет стоимость всех позиций счёта."""
        return round(
            sum(
                item["quantity"] * item["unit_price"]
                for item in self.items
            ),
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
        charges = sum(
            charge["amount"] for charge in self.additional_charges
        )
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

        self.additional_charges.append({
            "description": description,
            "amount": round(float(amount), 2),
        })

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
        return (
            self.status in ("issued", "partially_paid")
            and check_date > self.due_date
        )

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

        return (
            record_date is not None
            and self.period_start <= record_date <= self.period_end
        )

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
            if payment.status in (
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
            if payment.status in (
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
