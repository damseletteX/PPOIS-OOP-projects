"""Маршруты, транспортные заказы, доставки и рейсы."""

from datetime import date, datetime

from .cargo import Cargo
from .vehicles import Vehicle
from .exceptions import (
    InvalidRouteError,
    InvalidOrderStatusError,
    InvalidCargoError,
    CargoCapacityExceededError,
    DriverUnavailableError,
    VehicleUnavailableError,
    DeliveryError,
)


class RoutePoint:
    """Отдельная точка маршрута."""

    def __init__(
        self,
        point_id: str,
        address: str,
        sequence_number: int,
        planned_arrival: datetime | None = None,
    ):
        if not point_id or not address:
            raise InvalidRouteError("ID точки и адрес обязательны.")
        if sequence_number < 1:
            raise InvalidRouteError("Номер точки должен быть положительным.")

        self.point_id = point_id
        self.address = address
        self.sequence_number = sequence_number
        self.planned_arrival = planned_arrival
        self.actual_arrival = None
        self.is_completed = False
        self.notes = ""

    def record_arrival(self, arrival_time: datetime | None = None):
        """Фиксирует фактическое прибытие в точку."""
        self.actual_arrival = arrival_time or datetime.now()
        self.is_completed = True

    def set_planned_arrival(self, arrival_time: datetime):
        """Устанавливает плановое время прибытия."""
        self.planned_arrival = arrival_time

    def delay_minutes(self) -> int:
        """Вычисляет задержку относительно планового прибытия."""
        if self.planned_arrival is None or self.actual_arrival is None:
            return 0
        delay = self.actual_arrival - self.planned_arrival
        return max(0, int(delay.total_seconds() // 60))

    def add_note(self, note: str):
        """Добавляет примечание к точке маршрута."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()


class Route:
    """Маршрут перевозки."""

    def __init__(
        self,
        route_id: str,
        name: str,
        origin: str,
        destination: str,
        distance_km: float,
    ):
        if not route_id or not name or not origin or not destination:
            raise InvalidRouteError("Заполните основные данные маршрута.")
        if origin == destination:
            raise InvalidRouteError("Начало и конец маршрута совпадают.")
        if distance_km <= 0:
            raise InvalidRouteError("Длина маршрута должна быть положительной.")

        self.route_id = route_id
        self.name = name
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.points = []
        self.is_active = True
        self.estimated_duration_hours = 0.0
        self.restrictions = []
        self.toll_cost = 0.0

    def add_point(self, point: RoutePoint):
        """Добавляет промежуточную точку маршрута."""
        if any(p.point_id == point.point_id for p in self.points):
            raise InvalidRouteError("Такая точка уже есть в маршруте.")
        if any(p.sequence_number == point.sequence_number for p in self.points):
            raise InvalidRouteError("Номер точки уже используется.")
        self.points.append(point)
        self.points.sort(key=lambda p: p.sequence_number)

    def remove_point(self, point_id: str) -> bool:
        """Удаляет точку маршрута по ID."""
        for point in self.points:
            if point.point_id == point_id:
                self.points.remove(point)
                return True
        return False

    def calculate_duration(self, average_speed_kmh: float) -> float:
        """Оценивает время движения без учёта остановок."""
        if average_speed_kmh <= 0:
            raise InvalidRouteError("Средняя скорость должна быть положительной.")
        self.estimated_duration_hours = self.distance_km / average_speed_kmh
        return self.estimated_duration_hours

    def calculate_cost(self, cost_per_km: float) -> float:
        """Вычисляет стоимость маршрута по цене за километр."""
        if cost_per_km < 0:
            raise InvalidRouteError("Цена за километр не может быть отрицательной.")
        return self.distance_km * cost_per_km + self.toll_cost

    def add_restriction(self, restriction: str):
        """Добавляет ограничение маршрута."""
        if not restriction:
            raise InvalidRouteError("Ограничение не может быть пустым.")
        self.restrictions.append(restriction)

    def set_active(self, active: bool):
        """Включает или отключает маршрут."""
        self.is_active = active

    def get_next_point(self) -> RoutePoint | None:
        """Возвращает ближайшую незавершённую точку."""
        for point in self.points:
            if not point.is_completed:
                return point
        return None

    def progress_percentage(self) -> float:
        """Вычисляет долю пройденных промежуточных точек."""
        if not self.points:
            return 100.0
        completed = sum(point.is_completed for point in self.points)
        return completed / len(self.points) * 100


class OrderItem:
    """Позиция транспортного заказа."""

    def __init__(
        self,
        item_id: str,
        cargo: Cargo,
        quantity: int = 1,
    ):
        if not item_id:
            raise InvalidCargoError("ID позиции заказа обязателен.")
        if quantity < 1:
            raise InvalidCargoError("Количество должно быть не меньше единицы.")

        self.item_id = item_id
        self.cargo = cargo
        self.quantity = quantity
        self.unit_price = 0.0
        self.special_instructions = ""
        self.is_loaded = False
        self.is_unloaded = False

    def total_weight(self) -> float:
        """Возвращает общий вес груза в позиции."""
        return self.cargo.weight_kg * self.quantity

    def total_volume(self) -> float:
        """Возвращает общий объём груза в позиции."""
        return self.cargo.volume_m3 * self.quantity

    def calculate_price(self) -> float:
        """Рассчитывает стоимость позиции."""
        return self.unit_price * self.quantity

    def set_unit_price(self, price: float):
        """Устанавливает цену за одну единицу груза."""
        if price < 0:
            raise InvalidCargoError("Цена не может быть отрицательной.")
        self.unit_price = price

    def set_instructions(self, instructions: str):
        """Устанавливает особые инструкции для перевозки."""
        self.special_instructions = instructions

    def mark_loaded(self):
        """Отмечает позицию как загруженную."""
        self.is_loaded = True
        self.is_unloaded = False

    def mark_unloaded(self):
        """Отмечает позицию как выгруженную."""
        if not self.is_loaded:
            raise DeliveryError("Нельзя выгрузить незагруженный груз.")
        self.is_unloaded = True


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


class Shipment:
    """Подготовленная партия груза."""

    def __init__(
        self,
        shipment_id: str,
        order: TransportOrder,
        prepared_date: date | None = None,
    ):
        if not shipment_id:
            raise InvalidOrderStatusError("ID отправления обязателен.")

        self.shipment_id = shipment_id
        self.order = order
        self.prepared_date = prepared_date or date.today()
        self.items = list(order.items)
        self.is_ready = False
        self.loaded_vehicle = None
        self.loading_time = None
        self.unloading_time = None
        self.seal_number = ""

    def check_readiness(self) -> bool:
        """Проверяет готовность отправления к перевозке."""
        return bool(self.items) and all(item.cargo.is_packed for item in self.items)

    def prepare(self):
        """Подтверждает готовность отправления."""
        if not self.check_readiness():
            raise DeliveryError("Не все грузы упакованы или отправление пустое.")
        self.is_ready = True

    def load_onto(self, vehicle: Vehicle):
        """Загружает отправление на подходящий транспорт."""
        if not self.is_ready:
            raise DeliveryError("Сначала подготовьте отправление.")
        if not vehicle.is_available:
            raise VehicleUnavailableError("Транспорт недоступен.")

        if hasattr(vehicle, "tank_volume_liters"):
            raise InvalidCargoError(
                "Для цистерны требуется отдельная проверка совместимости груза."
            )

        total_weight = sum(item.total_weight() for item in self.items)
        total_volume = sum(item.total_volume() for item in self.items)

        if total_weight > vehicle.capacity_kg:
            raise CargoCapacityExceededError("Превышена грузоподъёмность.")

        vehicle_volume = getattr(vehicle, "cargo_volume_m3", None)
        if vehicle_volume is not None and total_volume > vehicle_volume:
            raise CargoCapacityExceededError("Превышен объём кузова.")

        self.loaded_vehicle = vehicle
        self.loading_time = datetime.now()

        for item in self.items:
            item.mark_loaded()

        vehicle.mark_unavailable()

    def unload(self):
        """Фиксирует выгрузку отправления."""
        if self.loaded_vehicle is None:
            raise DeliveryError("Отправление ещё не загружено.")

        for item in self.items:
            item.mark_unloaded()

        self.unloading_time = datetime.now()
        self.loaded_vehicle.mark_available()
        self.loaded_vehicle = None

    def set_seal_number(self, seal_number: str):
        """Устанавливает номер пломбы отправления."""
        if not seal_number:
            raise DeliveryError("Номер пломбы не может быть пустым.")
        self.seal_number = seal_number


class Stop:
    """Остановка во время рейса."""

    def __init__(
        self,
        stop_id: str,
        address: str,
        purpose: str = "other",
    ):
        if not stop_id or not address:
            raise InvalidRouteError("ID остановки и адрес обязательны.")
        if purpose not in {"loading", "unloading", "rest", "fuel", "other"}:
            raise InvalidRouteError("Неизвестная цель остановки.")

        self.stop_id = stop_id
        self.address = address
        self.purpose = purpose
        self.planned_time = None
        self.actual_time = None
        self.duration_minutes = 0
        self.is_completed = False
        self.notes = ""

    def schedule(self, planned_time: datetime, duration_minutes: int = 0):
        """Назначает время и длительность остановки."""
        if duration_minutes < 0:
            raise InvalidRouteError("Длительность не может быть отрицательной.")
        self.planned_time = planned_time
        self.duration_minutes = duration_minutes

    def complete(self, actual_time: datetime | None = None):
        """Отмечает остановку как завершённую."""
        self.actual_time = actual_time or datetime.now()
        self.is_completed = True

    def delay_minutes(self) -> int:
        """Вычисляет задержку начала остановки."""
        if self.planned_time is None or self.actual_time is None:
            return 0
        delay = self.actual_time - self.planned_time
        return max(0, int(delay.total_seconds() // 60))

    def add_note(self, note: str):
        """Добавляет примечание к остановке."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()


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


class Delivery:
    """Доставка заказа получателю."""

    def __init__(
        self,
        delivery_id: str,
        order: TransportOrder,
        recipient: str,
        address: str,
        scheduled_date: date,
    ):
        if not delivery_id or not recipient or not address:
            raise DeliveryError("ID, получатель и адрес доставки обязательны.")

        self.delivery_id = delivery_id
        self.order = order
        self.recipient = recipient
        self.address = address
        self.scheduled_date = scheduled_date
        self.status = "scheduled"
        self.actual_delivery_time = None
        self.received_by = ""
        self.proof_of_delivery = ""
        self.failure_reason = ""

    def mark_in_transit(self):
        """Отмечает, что доставка находится в пути."""
        if self.status != "scheduled":
            raise DeliveryError("Доставку нельзя перевести в этот статус.")
        self.status = "in_transit"

    def confirm_delivery(self, received_by: str, proof: str = ""):
        """Подтверждает вручение заказа."""
        if self.status != "in_transit":
            raise DeliveryError("Подтвердить можно только доставку в пути.")
        if not received_by:
            raise DeliveryError("Укажите, кто принял груз.")

        self.received_by = received_by
        self.proof_of_delivery = proof
        self.actual_delivery_time = datetime.now()
        self.status = "delivered"

        if self.order.status == "in_transit":
            self.order.set_status("delivered")

    def report_failure(self, reason: str):
        """Фиксирует неудачную попытку доставки."""
        if self.status == "delivered":
            raise DeliveryError("Уже доставленную посылку нельзя отметить неудачной.")
        if not reason:
            raise DeliveryError("Укажите причину неудачной доставки.")
        self.failure_reason = reason
        self.status = "failed"

    def reschedule(self, new_date: date):
        """Переносит дату доставки."""
        if self.status == "delivered":
            raise DeliveryError("Нельзя перенести уже завершённую доставку.")
        if new_date < date.today():
            raise DeliveryError("Новая дата не может быть в прошлом.")
        self.scheduled_date = new_date
        self.status = "scheduled"

    def is_late(self, today: date | None = None) -> bool:
        """Проверяет просрочку ещё не завершённой доставки."""
        today = today or date.today()
        return self.status != "delivered" and today > self.scheduled_date

    def record_recipient(self, recipient: str):
        """Обновляет имя получателя."""
        if not recipient:
            raise DeliveryError("Имя получателя не может быть пустым.")
        self.recipient = recipient


class Schedule:
    """Расписание рейсов."""

    def __init__(self, schedule_id: str, name: str):
        if not schedule_id or not name:
            raise InvalidRouteError("ID и название расписания обязательны.")

        self.schedule_id = schedule_id
        self.name = name
        self.trips = []
        self.is_active = True
        self.created_at = date.today()
        self.notes = ""

    def add_trip(self, trip: Trip):
        """Добавляет рейс, если время и ресурсы не конфликтуют."""
        if not self.is_active:
            raise InvalidRouteError("Расписание неактивно.")
        if any(existing.trip_id == trip.trip_id for existing in self.trips):
            raise InvalidRouteError("Этот рейс уже есть в расписании.")

        for existing in self.trips:
            if existing.status in {"completed", "cancelled"}:
                continue
            if existing.driver is trip.driver or existing.vehicle is trip.vehicle:
                if existing.departure_time == trip.departure_time:
                    raise InvalidRouteError("В это время водитель или транспорт уже назначен.")

        self.trips.append(trip)
        self.trips.sort(key=lambda item: item.departure_time)

    def remove_trip(self, trip_id: str) -> bool:
        """Удаляет запланированный рейс из расписания."""
        for trip in self.trips:
            if trip.trip_id == trip_id:
                if trip.status != "planned":
                    raise InvalidRouteError("Можно удалить только ещё не начатый рейс.")
                self.trips.remove(trip)
                return True
        return False

    def get_trips_for_date(self, target_date: date) -> list[Trip]:
        """Возвращает рейсы, назначенные на выбранную дату."""
        return [trip for trip in self.trips if trip.departure_time.date() == target_date]

    def get_available_trips(self) -> list[Trip]:
        """Возвращает рейсы, которые ещё не начались."""
        return [trip for trip in self.trips if trip.status == "planned"]

    def cancel_schedule(self):
        """Отключает расписание и отменяет запланированные рейсы."""
        self.is_active = False
        for trip in self.trips:
            if trip.status == "planned":
                trip.cancel("Расписание отменено")

    def add_note(self, note: str):
        """Добавляет примечание к расписанию."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()
