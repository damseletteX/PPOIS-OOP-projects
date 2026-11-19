from datetime import date

from ..exceptions import (
    InvalidDriverError,
)


class Department:
    """Подразделение транспортной компании."""

    def __init__(
        self,
        department_id: str,
        name: str,
        description: str = "",
        manager=None,
        monthly_target: float = 0.0,
    ):
        if not department_id or not name:
            raise ValueError("Не указаны данные подразделения.")
        if monthly_target < 0:
            raise ValueError("План подразделения не может быть отрицательным.")

        self.department_id = department_id
        self.name = name
        self.description = description
        self.manager = manager
        self.employees = []
        self.budget = 0.0
        self.monthly_target = monthly_target
        self.expenses = []
        self.is_active = True
        self.creation_date = date.today()
        self.notes = []

    def add_employee(self, employee):
        """Добавляет сотрудника в подразделение."""
        if employee in self.employees:
            raise ValueError("Сотрудник уже находится в подразделении.")

        self.employees.append(employee)
        employee.department = self.name

    def remove_employee(self, employee):
        """Удаляет сотрудника из подразделения."""
        if employee not in self.employees:
            return False

        self.employees.remove(employee)
        employee.department = None

        if self.manager is employee:
            self.manager = None

        return True

    def assign_manager(self, manager):
        """Назначает руководителя подразделения."""
        if manager not in self.employees:
            raise ValueError("Руководитель должен быть сотрудником подразделения.")

        self.manager = manager

    def change_manager(self, new_manager):
        """Меняет руководителя подразделения."""
        return self.assign_manager(new_manager)

    def set_budget(self, amount: float):
        """Устанавливает бюджет подразделения."""
        if amount < 0:
            raise ValueError("Бюджет не может быть отрицательным.")

        self.budget = round(float(amount), 2)

    def add_expense(self, expense):
        """Добавляет расход подразделения."""
        if expense not in self.expenses:
            self.expenses.append(expense)

    def calculate_expenses(self):
        """Считает подтверждённые расходы подразделения."""
        return round(
            sum(
                expense.amount
                for expense in self.expenses
                if expense.status in ("approved", "reimbursed")
            ),
            2,
        )

    def calculate_remaining_budget(self):
        """Вычисляет остаток бюджета."""
        return round(self.budget - self.calculate_expenses(), 2)

    def calculate_payroll(self):
        """Считает сумму зарплат сотрудников подразделения."""
        return round(
            sum(getattr(employee, "salary", 0) for employee in self.employees),
            2,
        )

    def find_employee(self, employee_id: str):
        """Находит сотрудника подразделения по идентификатору."""
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def assign_task(self, employee_id: str, task: str):
        """Передаёт задачу конкретному сотруднику."""
        employee = self.find_employee(employee_id)

        if employee is None:
            raise InvalidDriverError("Сотрудник не найден в этом подразделении.")

        if not callable(getattr(employee, "assign_task", None)):
            raise InvalidDriverError("Сотрудник не поддерживает назначение задач.")

        employee.assign_task(task)

    def set_monthly_target(self, target: float):
        """Изменяет плановый показатель подразделения."""
        if target < 0:
            raise ValueError("План не может быть отрицательным.")

        self.monthly_target = round(float(target), 2)

    def activate(self):
        """Активирует подразделение."""
        self.is_active = True

    def deactivate(self):
        """Деактивирует подразделение."""
        if self.employees:
            raise ValueError("Перед отключением подразделения необходимо распределить сотрудников.")

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание подразделения."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)