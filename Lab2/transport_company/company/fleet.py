from ..exceptions import (
    InvalidDriverError,
    InvalidVehicleError,
    VehicleUnavailableError,
)


class Fleet:
    """Автопарк транспортной компании."""

    def __init__(
        self,
        fleet_id: str,
        name: str,
        max_vehicle_count: int = 100,
    ):
        if not fleet_id or not name:
            raise ValueError("Не указаны идентификатор или название автопарка.")
        if max_vehicle_count <= 0:
            raise ValueError("Размер автопарка должен быть положительным.")

        self.fleet_id = fleet_id
        self.name = name
        self.max_vehicle_count = max_vehicle_count
        self.vehicles = {}
        self.assigned_drivers = {}
        self.trip_history = []
        self.maintenance_records = []
        self.is_active = True
        self.notes = []

    def add_vehicle(self, vehicle):
        """Добавляет транспортное средство в автопарк."""
        vehicle_id = getattr(vehicle, "vehicle_id", None)

        if not vehicle_id:
            raise InvalidVehicleError("У транспорта отсутствует идентификатор.")
        if vehicle_id in self.vehicles:
            raise InvalidVehicleError("Транспорт уже есть в автопарке.")
        if len(self.vehicles) >= self.max_vehicle_count:
            raise InvalidVehicleError("Достигнут лимит автопарка.")

        self.vehicles[vehicle_id] = vehicle

    def remove_vehicle(self, vehicle_id: str):
        """Удаляет свободное транспортное средство."""
        vehicle = self.vehicles.get(vehicle_id)

        if vehicle is None:
            return False
        if not vehicle.is_available:
            raise VehicleUnavailableError("Нельзя удалить используемое транспортное средство.")

        for driver_id, driver in list(self.assigned_drivers.items()):
            if getattr(driver, "assigned_vehicle", None) is vehicle:
                raise InvalidVehicleError("Сначала необходимо отвязать водителя от транспорта.")

        del self.vehicles[vehicle_id]
        return True

    def get_vehicle(self, vehicle_id: str):
        """Находит транспорт по идентификатору."""
        return self.vehicles.get(vehicle_id)

    def get_available_vehicles(self):
        """Возвращает свободный транспорт."""
        return [vehicle for vehicle in self.vehicles.values() if vehicle.is_available]

    def get_unavailable_vehicles(self):
        """Возвращает занятый или недоступный транспорт."""
        return [vehicle for vehicle in self.vehicles.values() if not vehicle.is_available]

    def find_by_registration(self, registration_number: str):
        """Находит транспорт по регистрационному номеру."""
        for vehicle in self.vehicles.values():
            if vehicle.registration_number == registration_number:
                return vehicle

        return None

    def assign_driver(self, driver, vehicle_id: str):
        """Назначает водителя на транспортное средство."""
        vehicle = self.get_vehicle(vehicle_id)

        if vehicle is None:
            raise InvalidVehicleError("Транспорт не найден.")
        if not vehicle.is_available:
            raise VehicleUnavailableError("Транспорт уже занят.")

        driver_id = getattr(driver, "employee_id", None)

        if not driver_id:
            raise InvalidDriverError("У водителя отсутствует идентификатор.")
        if driver_id in self.assigned_drivers:
            raise InvalidDriverError("Водитель уже числится в автопарке.")

        driver.assign_vehicle(vehicle)
        self.assigned_drivers[driver_id] = driver

    def unassign_driver(self, driver_id: str):
        """Отвязывает водителя от транспортного средства."""
        driver = self.assigned_drivers.get(driver_id)

        if driver is None:
            return False
        if not driver.is_available:
            raise InvalidDriverError("Нельзя отвязать водителя во время поездки.")

        driver.assigned_vehicle = None
        del self.assigned_drivers[driver_id]
        return True

    def register_trip(self, trip):
        """Добавляет поездку в историю автопарка."""
        if trip.vehicle.vehicle_id not in self.vehicles:
            raise InvalidVehicleError("Транспорт поездки не принадлежит этому автопарку.")
        if trip in self.trip_history:
            raise ValueError("Поездка уже зарегистрирована.")

        self.trip_history.append(trip)

    def get_vehicle_trips(self, vehicle_id: str):
        """Возвращает поездки конкретного автомобиля."""
        return [trip for trip in self.trip_history if trip.vehicle.vehicle_id == vehicle_id]

    def get_vehicles_by_fuel(self, fuel_type: str):
        """Фильтрует транспорт по типу топлива."""
        return [vehicle for vehicle in self.vehicles.values() if vehicle.fuel_type == fuel_type]

    def calculate_total_capacity(self):
        """Считает суммарную грузоподъёмность автопарка."""
        return round(
            sum(vehicle.capacity_kg for vehicle in self.vehicles.values()),
            2,
        )

    def calculate_average_mileage(self):
        """Вычисляет средний пробег транспортных средств."""
        if not self.vehicles:
            return 0.0

        return round(
            sum(vehicle.mileage_km for vehicle in self.vehicles.values()) / len(self.vehicles),
            2,
        )

    def get_vehicles_needing_inspection(self):
        """Находит автомобили, которым нужна проверка."""
        return [vehicle for vehicle in self.vehicles.values() if vehicle.needs_inspection()]

    def add_maintenance_record(self, record):
        """Сохраняет запись о техническом обслуживании."""
        if record.vehicle.vehicle_id not in self.vehicles:
            raise InvalidVehicleError("Транспорт не принадлежит этому автопарку.")

        self.maintenance_records.append(record)

    def activate(self):
        """Активирует автопарк."""
        self.is_active = True

    def deactivate(self):
        """Отключает автопарк для новых назначений."""
        if self.get_unavailable_vehicles():
            raise VehicleUnavailableError("Нельзя отключить автопарк с занятыми автомобилями.")

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание к автопарку."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)