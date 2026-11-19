from .person import Person


class Customer(Person):
    """Общий класс клиентов транспортной компании."""

    def __init__(self, name: str, phone: str, address: str, email: str = ""):
        super().__init__(name, phone, email)
        if not address.strip():
            raise ValueError("Адрес не может быть пустым.")

        self.address = address.strip()
        self.orders = []
        self.discount_percent = 0
        self.is_verified = False

    def add_order(self, order) -> None:
        if not self.is_active:
            raise ValueError("Неактивный клиент не может оформлять заказы.")
        if order in self.orders:
            raise ValueError("Этот заказ уже добавлен клиенту.")
        self.orders.append(order)

    def remove_order(self, order) -> None:
        if order not in self.orders:
            raise ValueError("Заказ не найден у этого клиента.")
        self.orders.remove(order)

    def verify_customer(self) -> None:
        self.is_verified = True

    def set_discount(self, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Скидка должна быть от 0 до 100%.")
        self.discount_percent = percent

    def calculate_discount(self, amount: float) -> float:
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной.")
        return amount * self.discount_percent / 100

    def get_order_count(self) -> int:
        return len(self.orders)

    def change_address(self, address: str) -> None:
        if not address.strip():
            raise ValueError("Адрес не может быть пустым.")
        self.address = address.strip()