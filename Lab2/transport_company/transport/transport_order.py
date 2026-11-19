from datetime import date
from .order_item import OrderItem
from .route import Route
from ..exceptions import (
    InvalidRouteError,
    InvalidOrderStatusError,
    InvalidCargoError,
)


class TransportOrder:
    """Заказ клиента на перевозку."""

    ALLOWED_STATUSES = {
        "new",
        "pending",
        "approved",
        "in_transit",
        "delivered",
        "cancelled",
    }

    def __init__(
        self,
        order_id: str,
        customer,
        origin: str,
        destination: str,
        created_at: date | None = None,
    ):
        if not order_id or not origin or not destination:
            raise InvalidOrderStatusError("ID заказа, отправление и назначение обязательны.")
        if origin == destination:
            raise InvalidRouteError("Отправление и назначение совпадают.")

        self.order_id = order_id
        self.customer = customer
        self.origin = origin
        self.destination = destination
        self.created_at = created_at or date.today()
        self.status = "new"
        self.items = []
        self.route = None
        self.assigned_trip = None
        self.notes = ""
        self.priority = "normal"
        self.requested_delivery_date = None

        if hasattr(customer, "add_order"):
            customer.add_order(self)

    def add_item(self, item: OrderItem):
        """Добавляет позицию в заказ."""
        if self.status not in {"new", "pending"}:
            raise InvalidOrderStatusError(
                "Добавлять грузы можно только в новый или ожидающий заказ."
            )
        if any(existing.item_id == item.item_id for existing in self.items):
            raise InvalidCargoError("Позиция с таким ID уже добавлена.")
        self.items.append(item)

    def remove_item(self, item_id: str) -> bool:
        """Удаляет позицию из заказа по ID."""
        if self.status not in {"new", "pending"}:
            raise InvalidOrderStatusError("Изменять этот заказ уже нельзя.")
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                return True
        return False

    def set_route(self, route: Route):
        """Назначает заказу маршрут."""
        if not route.is_active:
            raise InvalidRouteError("Нельзя назначить неактивный маршрут.")
        if route.origin != self.origin or route.destination != self.destination:
            raise InvalidRouteError("Маршрут не соответствует заказу.")
        self.route = route

    def set_status(self, new_status: str):
        """Меняет статус заказа с проверкой допустимого перехода."""
        transitions = {
            "new": {"pending", "approved", "cancelled"},
            "pending": {"approved", "cancelled"},
            "approved": {"in_transit", "cancelled"},
            "in_transit": {"delivered"},
            "delivered": set(),
            "cancelled": set(),
        }

        if new_status not in self.ALLOWED_STATUSES:
            raise InvalidOrderStatusError("Неизвестный статус заказа.")
        if new_status not in transitions[self.status]:
            raise InvalidOrderStatusError(
                f"Нельзя изменить статус с {self.status} на {new_status}."
            )
        self.status = new_status

    def submit_for_approval(self):
        """Отправляет новый заказ на рассмотрение."""
        self.set_status("pending")

    def approve(self):
        """Подтверждает заказ."""
        self.set_status("approved")

    def cancel(self, reason: str = ""):
        """Отменяет заказ до начала перевозки."""
        self.set_status("cancelled")
        self.notes = f"{self.notes}\nПричина отмены: {reason}".strip()

    def total_weight(self) -> float:
        """Считает суммарный вес всех позиций."""
        return sum(item.total_weight() for item in self.items)

    def total_volume(self) -> float:
        """Считает суммарный объём всех позиций."""
        return sum(item.total_volume() for item in self.items)

    def calculate_items_cost(self) -> float:
        """Считает суммарную стоимость позиций."""
        return sum(item.calculate_price() for item in self.items)

    def assign_trip(self, trip):
        """Связывает заказ с рейсом."""
        if self.status != "approved":
            raise InvalidOrderStatusError("Назначить рейс можно только подтверждённому заказу.")
        if self.assigned_trip is not None:
            raise InvalidOrderStatusError("Заказ уже назначен на рейс.")
        trip.add_order(self)

    def set_priority(self, priority: str):
        """Устанавливает приоритет заказа."""
        if priority not in {"low", "normal", "high", "urgent"}:
            raise InvalidOrderStatusError("Неизвестный приоритет.")
        self.priority = priority

    def set_delivery_deadline(self, deadline: date):
        """Устанавливает желаемую дату доставки."""
        if deadline < self.created_at:
            raise InvalidOrderStatusError("Дата доставки не может быть раньше создания заказа.")
        self.requested_delivery_date = deadline