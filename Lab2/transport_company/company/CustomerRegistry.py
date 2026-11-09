from datetime import datetime
from ..people.CorporateCustomer import CorporateCustomer
from ..exceptions import (
    InvalidCustomerError,
)


class CustomerRegistry:
    """Реестр клиентов транспортной компании."""

    def __init__(self):
        self.customers = {}
        self.registration_history = []
        self.last_updated = datetime.now()

    def register(self, customer):
        """Добавляет нового клиента."""
        customer_id = getattr(customer, "customer_id", None)

        if not customer_id:
            raise InvalidCustomerError("У клиента отсутствует идентификатор.")
        if customer_id in self.customers:
            raise InvalidCustomerError("Клиент уже зарегистрирован.")

        self.customers[customer_id] = customer
        self.registration_history.append(f"Зарегистрирован клиент {customer_id}")
        self.last_updated = datetime.now()

    def unregister(self, customer_id: str):
        """Удаляет клиента, у которого нет активных заказов."""
        customer = self.customers.get(customer_id)

        if customer is None:
            return False

        active_orders = [
            order
            for order in getattr(customer, "orders", [])
            if getattr(order, "status", None) not in ("delivered", "cancelled")
        ]

        if active_orders:
            raise InvalidCustomerError("Нельзя удалить клиента с активными заказами.")

        del self.customers[customer_id]
        self.registration_history.append(f"Удалён клиент {customer_id}")
        self.last_updated = datetime.now()
        return True

    def get_customer(self, customer_id: str):
        """Находит клиента по идентификатору."""
        return self.customers.get(customer_id)

    def find_by_name(self, name: str):
        """Ищет клиентов по имени или названию организации."""
        search_name = name.lower()

        return [
            customer for customer in self.customers.values() if search_name in customer.name.lower()
        ]

    def get_active_customers(self):
        """Возвращает список активных клиентов."""
        return [
            customer for customer in self.customers.values() if getattr(customer, "is_active", True)
        ]

    def get_corporate_customers(self):
        """Возвращает корпоративных клиентов."""
        return [
            customer
            for customer in self.customers.values()
            if isinstance(customer, CorporateCustomer)
        ]

    def get_customers_with_orders(self):
        """Возвращает клиентов, у которых есть заказы."""
        return [customer for customer in self.customers.values() if getattr(customer, "orders", [])]

    def get_customers_without_orders(self):
        """Возвращает клиентов без заказов."""
        return [
            customer for customer in self.customers.values() if not getattr(customer, "orders", [])
        ]

    def count_customers(self):
        """Возвращает количество зарегистрированных клиентов."""
        return len(self.customers)

    def calculate_total_orders(self):
        """Считает общее количество заказов клиентов."""
        return sum(len(getattr(customer, "orders", [])) for customer in self.customers.values())

    def get_customer_order_history(self, customer_id: str):
        """Возвращает историю заказов конкретного клиента."""
        customer = self.get_customer(customer_id)

        if customer is None:
            raise InvalidCustomerError("Клиент не найден.")

        return list(getattr(customer, "orders", []))

    def update_status(self, customer_id: str, active: bool):
        """Изменяет активность клиента."""
        customer = self.get_customer(customer_id)

        if customer is None:
            raise InvalidCustomerError("Клиент не найден.")

        if active:
            customer.activate()
        else:
            customer.deactivate()

        self.last_updated = datetime.now()