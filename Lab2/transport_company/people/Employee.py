from .Person import Person


class Employee(Person):
    """Базовый класс сотрудника."""

    def __init__(self, name: str, phone: str, employee_id: str, salary: float, email: str = ""):
        super().__init__(name, phone, email)
        if not employee_id.strip():
            raise ValueError("Табельный номер обязателен.")
        if salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")

        self.employee_id = employee_id.strip()
        self.salary = salary
        self.department = "Transport"
        self.is_available = True
        self.assigned_tasks = []

    def assign_task(self, task: str) -> None:
        if not self.is_active:
            raise ValueError("Нельзя назначить задачу неактивному сотруднику.")
        if not task.strip():
            raise ValueError("Описание задачи не может быть пустым.")
        self.assigned_tasks.append(task.strip())
        self.is_available = False

    def complete_task(self, task: str) -> None:
        if task not in self.assigned_tasks:
            raise ValueError("Такая задача сотруднику не назначена.")
        self.assigned_tasks.remove(task)
        self.is_available = len(self.assigned_tasks) == 0

    def change_department(self, department: str) -> None:
        if not department.strip():
            raise ValueError("Название отдела не может быть пустым.")
        self.department = department.strip()

    def calculate_annual_salary(self) -> float:
        return self.salary * 12

    def is_ready_for_work(self) -> bool:
        return self.is_active and self.is_available