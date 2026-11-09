from .Customer import Customer
from .Employee import Employee


class Manager(Employee):
    """Менеджер, отвечающий за клиентов и заказы."""

    def __init__(self, name: str, phone: str, employee_id: str, salary: float, email: str = ""):
        super().__init__(name, phone, employee_id, salary, email)
        self.managed_customers = []
        self.approved_orders = []
        self.monthly_target = 0.0
        self.monthly_revenue = 0.0

    def register_customer(self, customer: Customer) -> None:
        if customer in self.managed_customers:
            raise ValueError("Клиент уже закреплён за менеджером.")
        self.managed_customers.append(customer)

    def approve_order(self, order) -> None:
        if not self.is_active:
            raise ValueError("Неактивный менеджер не может одобрять заказы.")
        if order in self.approved_orders:
            raise ValueError("Заказ уже одобрен.")

        status = getattr(order, "status", None)
        if status not in ("new", "pending"):
            raise ValueError("Можно одобрить только новый или ожидающий заказ.")

        order.status = "approved"
        self.approved_orders.append(order)

    def set_monthly_target(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("План выручки не может быть отрицательным.")
        self.monthly_target = amount

    def record_revenue(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Выручка не может быть отрицательной.")
        self.monthly_revenue += amount

    def calculate_target_completion(self) -> float:
        if self.monthly_target == 0:
            return 0.0
        return self.monthly_revenue / self.monthly_target * 100

    def remove_customer(self, customer: Customer) -> None:
        if customer not in self.managed_customers:
            raise ValueError("Клиент не закреплён за этим менеджером.")
        self.managed_customers.remove(customer)