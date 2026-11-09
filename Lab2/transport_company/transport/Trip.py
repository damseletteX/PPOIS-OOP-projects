from datetime import datetime
from .Route import Route
from .TransportOrder import TransportOrder
from .Stop import Stop
from ..vehicles.Vehicle import Vehicle
from ..exceptions import (
    InvalidRouteError,
    InvalidOrderStatusError,
    DriverUnavailableError,
    VehicleUnavailableError,
)


class Trip:
    """Рейс водителя и транспортного средства."""

    def __init__(
        self,
        trip_id: str,
        driver,
        vehicle: Vehicle,
        route: Route,
        departure_time: datetime,
    ):
        if not trip_id:
            raise InvalidRouteError("ID рейса обязателен.")
        if not route.is_active:
            raise InvalidRouteError("Нельзя выполнить неактивный маршрут.")

        self.trip_id = trip_id
        self.driver = driver
        self.vehicle = vehicle
        self.route = route
        self.departure_time = departure_time
        self.actual_departure = None
        self.arrival_time = None
        self.actual_arrival = None
        self.status = "planned"
        self.orders = []
        self.stops = []
        self.distance_travelled_km = 0.0
        self.notes = ""

    def add_order(self, order: TransportOrder):
        """Добавляет подтверждённый заказ в рейс."""
        if order.status != "approved":
            raise InvalidOrderStatusError("В рейс можно добавить только подтверждённый заказ.")
        if order.assigned_trip is not None and order.assigned_trip is not self:
            raise InvalidOrderStatusError("Заказ уже назначен на другой рейс.")
        if order.route is not None and order.route is not self.route:
            raise InvalidRouteError("Маршрут заказа не совпадает с рейсом.")

        if order not in self.orders:
            self.orders.append(order)
            order.assigned_trip = self

    def add_stop(self, stop: Stop):
        """Добавляет остановку в рейс."""
        if any(existing.stop_id == stop.stop_id for existing in self.stops):
            raise InvalidRouteError("Такая остановка уже есть в рейсе.")
        self.stops.append(stop)

    def start(self):
        """Начинает рейс, если водитель и транспорт доступны."""
        if self.status != "planned":
            raise InvalidOrderStatusError("Рейс уже начат или завершён.")
        if not self.vehicle.is_available:
            raise VehicleUnavailableError("Транспорт недоступен.")
        if not getattr(self.driver, "is_available", False):
            raise DriverUnavailableError("Водитель недоступен.")

        assigned_vehicle = getattr(self.driver, "assigned_vehicle", None)
        if assigned_vehicle is not self.vehicle:
            raise DriverUnavailableError("Водителю не назначено это транспортное средство.")

        self.actual_departure = datetime.now()
        self.driver.start_trip()
        self.vehicle.is_available = False
        self.status = "in_progress"

        for order in self.orders:
            if order.status == "approved":
                order.set_status("in_transit")

    def finish(self):
        """Завершает рейс и освобождает водителя и транспорт."""
        if self.status != "in_progress":
            raise InvalidOrderStatusError("Можно завершить только начатый рейс.")

        self.actual_arrival = datetime.now()
        self.arrival_time = self.actual_arrival
        self.distance_travelled_km = self.route.distance_km
        self.vehicle.mark_available()
        self.driver.finish_trip()
        self.status = "completed"

        for order in self.orders:
            if order.status == "in_transit":
                order.set_status("delivered")

    def cancel(self, reason: str = ""):
        """Отменяет ещё не начатый рейс."""
        if self.status != "planned":
            raise InvalidOrderStatusError("Начатый рейс нельзя отменить этим методом.")
        self.status = "cancelled"
        self.notes = f"{self.notes}\nПричина отмены: {reason}".strip()

    def calculate_duration_hours(self) -> float:
        """Вычисляет фактическую длительность рейса."""
        if self.actual_departure is None or self.actual_arrival is None:
            return 0.0
        seconds = (self.actual_arrival - self.actual_departure).total_seconds()
        return max(0.0, seconds / 3600)

    def calculate_average_speed(self) -> float:
        """Вычисляет среднюю скорость по фактическому времени рейса."""
        duration = self.calculate_duration_hours()
        if duration == 0:
            return 0.0
        return self.distance_travelled_km / duration

    def add_note(self, note: str):
        """Добавляет примечание к рейсу."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()