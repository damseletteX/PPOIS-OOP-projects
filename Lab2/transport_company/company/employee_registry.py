from datetime import datetime
from ..people.driver import Driver
from ..exceptions import (
    InvalidDriverError,
)


class EmployeeRegistry:
    """Реестр сотрудников транспортной компании."""

    def __init__(self):
        self.employees = {}
        self.registration_history = []
        self.last_updated = datetime.now()

    def register(self, employee):
        """Регистрирует нового сотрудника."""
        employee_id = getattr(employee, "employee_id", None)

        if not employee_id:
            raise InvalidDriverError("У сотрудника отсутствует идентификатор.")
        if employee_id in self.employees:
            raise InvalidDriverError("Сотрудник уже зарегистрирован.")

        self.employees[employee_id] = employee
        self.registration_history.append(f"Зарегистрирован сотрудник {employee_id}")
        self.last_updated = datetime.now()

    def unregister(self, employee_id: str):
        """Удаляет сотрудника из реестра."""
        employee = self.employees.get(employee_id)

        if employee is None:
            return False

        if getattr(employee, "assigned_vehicle", None) is not None:
            raise InvalidDriverError("Нельзя удалить водителя с назначенным транспортом.")

        del self.employees[employee_id]
        self.registration_history.append(f"Удалён сотрудник {employee_id}")
        self.last_updated = datetime.now()
        return True

    def get_employee(self, employee_id: str):
        """Находит сотрудника по идентификатору."""
        return self.employees.get(employee_id)

    def find_by_name(self, name: str):
        """Ищет сотрудников по имени."""
        search_name = name.lower()

        return [
            employee for employee in self.employees.values() if search_name in employee.name.lower()
        ]

    def get_active_employees(self):
        """Возвращает список активных сотрудников."""
        return [
            employee for employee in self.employees.values() if getattr(employee, "is_active", True)
        ]

    def get_drivers(self):
        """Возвращает сотрудников, являющихся водителями."""
        return [employee for employee in self.employees.values() if isinstance(employee, Driver)]

    def get_by_department(self, department_name: str):
        """Возвращает сотрудников выбранного отдела."""
        return [
            employee
            for employee in self.employees.values()
            if getattr(employee, "department", None) == department_name
        ]

    def change_employee_status(self, employee_id: str, active: bool):
        """Активирует или деактивирует сотрудника."""
        employee = self.get_employee(employee_id)

        if employee is None:
            raise InvalidDriverError("Сотрудник не найден.")

        if active:
            employee.activate()
        else:
            employee.deactivate()

        self.last_updated = datetime.now()

    def calculate_total_salary(self):
        """Считает сумму зарплат всех сотрудников."""
        return round(
            sum(getattr(employee, "salary", 0) for employee in self.employees.values()),
            2,
        )

    def count_employees(self):
        """Возвращает общее количество сотрудников."""
        return len(self.employees)

    def get_employee_ids(self):
        """Возвращает идентификаторы всех сотрудников."""
        return list(self.employees.keys())

    def clear_inactive(self):
        """Удаляет из реестра всех неактивных сотрудников."""
        inactive_ids = [
            employee_id
            for employee_id, employee in self.employees.items()
            if not getattr(employee, "is_active", True)
            and getattr(employee, "assigned_vehicle", None) is None
        ]

        for employee_id in inactive_ids:
            del self.employees[employee_id]

        self.last_updated = datetime.now()
        return len(inactive_ids)