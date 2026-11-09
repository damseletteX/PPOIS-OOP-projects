from datetime import date, datetime
from ..exceptions import (
    InvalidOrderStatusError,
)


class OrderRegistry:
    """Реестр транспортных заказов."""

    def __init__(self):
        self.orders = {}
        self.registration_history = []
        self.last_updated = datetime.now()

    def register(self, order):
        """Регистрирует транспортный заказ."""
        order_id = getattr(order, "order_id", None)

        if not order_id:
            raise InvalidOrderStatusError("У заказа отсутствует идентификатор.")
        if order_id in self.orders:
            raise InvalidOrderStatusError("Заказ уже зарегистрирован.")

        self.orders[order_id] = order
        self.registration_history.append(f"Зарегистрирован заказ {order_id}")
        self.last_updated = datetime.now()

    def unregister(self, order_id: str):
        """Удаляет новый или отменённый заказ из реестра."""
        order = self.orders.get(order_id)

        if order is None:
            return False

        if order.status not in ("new", "cancelled"):
            raise InvalidOrderStatusError("Нельзя удалить заказ в работе.")

        del self.orders[order_id]
        self.last_updated = datetime.now()
        return True

    def get_order(self, order_id: str):
        """Находит заказ по идентификатору."""
        return self.orders.get(order_id)

    def get_by_status(self, status: str):
        """Возвращает заказы с указанным статусом."""
        return [order for order in self.orders.values() if order.status == status]

    def get_by_customer(self, customer):
        """Возвращает заказы конкретного клиента."""
        return [order for order in self.orders.values() if order.customer is customer]

    def get_by_priority(self, priority: str):
        """Возвращает заказы с указанным приоритетом."""
        return [order for order in self.orders.values() if order.priority == priority]

    def get_overdue_orders(self, check_date: date | None = None):
        """Находит заказы, срок доставки которых истёк."""
        check_date = check_date or date.today()

        return [
            order
            for order in self.orders.values()
            if order.requested_delivery_date is not None
            and order.requested_delivery_date < check_date
            and order.status not in ("delivered", "cancelled")
        ]

    def calculate_total_weight(self):
        """Считает общий вес всех зарегистрированных заказов."""
        return round(
            sum(order.total_weight() for order in self.orders.values()),
            2,
        )

    def calculate_total_value(self):
        """Считает общую стоимость позиций всех заказов."""
        return round(
            sum(order.calculate_items_cost() for order in self.orders.values()),
            2,
        )

    def count_orders(self):
        """Возвращает количество зарегистрированных заказов."""
        return len(self.orders)

    def count_by_status(self, status: str):
        """Считает количество заказов с указанным статусом."""
        return len(self.get_by_status(status))

    def cancel_order(self, order_id: str):
        """Отменяет заказ, если это допускает его текущий статус."""
        order = self.get_order(order_id)

        if order is None:
            raise InvalidOrderStatusError("Заказ не найден.")

        order.cancel()
        self.last_updated = datetime.now()

    def get_orders_for_period(
        self,
        start_date: date,
        end_date: date,
    ):
        """Возвращает заказы, созданные в указанном периоде."""
        if end_date < start_date:
            raise ValueError("Некорректный период.")

        result = []

        for order in self.orders.values():
            created_at = order.created_at

            # Если дата содержит время, преобразуем её в date.
            if isinstance(created_at, datetime):
                created_at = created_at.date()

            # Сравниваем даты.
            if isinstance(created_at, date) and start_date <= created_at <= end_date:
                result.append(order)

        return result

    def get_order_statistics(self):
        """Формирует статистику по статусам заказов."""
        statistics = {}

        for order in self.orders.values():
            statistics[order.status] = statistics.get(order.status, 0) + 1

        return statistics