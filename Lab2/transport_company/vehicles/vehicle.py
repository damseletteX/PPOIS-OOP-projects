from datetime import date

from ..exceptions import (
    InvalidVehicleError,
    VehicleUnavailableError,
)


class Vehicle:
    """Базовый класс транспортного средства."""

    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        year: int,
        registration_number: str,
        capacity_kg: float,
        required_license_category: str = "B",
        fuel_type: str = "diesel",
    ):
        if not vehicle_id or not brand or not model:
            raise InvalidVehicleError("ID, марка и модель обязательны.")
        if year < 1900 or year > date.today().year + 1:
            raise InvalidVehicleError("Некорректный год выпуска.")
        if capacity_kg <= 0:
            raise InvalidVehicleError("Грузоподъёмность должна быть положительной.")
        if not registration_number:
            raise InvalidVehicleError("Укажите регистрационный номер.")

        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.year = year
        self.registration_number = registration_number
        self.capacity_kg = capacity_kg
        self.required_license_category = required_license_category
        self.fuel_type = fuel_type
        self.mileage_km = 0.0
        self.is_available = True
        self.current_location = "Автопарк"
        self.inspections = []
        self.maintenance_records = []
        self.fuel_records = []

    def mark_unavailable(self):
        """Помечает транспорт как занятый."""
        if not self.is_available:
            raise VehicleUnavailableError("Транспорт уже занят.")
        self.is_available = False

    def mark_available(self):
        """Возвращает транспорт в доступное состояние."""
        self.is_available = True

    def update_mileage(self, new_mileage: float):
        """Обновляет пробег, не позволяя ему уменьшаться."""
        if new_mileage < self.mileage_km:
            raise InvalidVehicleError("Новый пробег не может быть меньше текущего.")
        self.mileage_km = new_mileage

    def can_transport(self, cargo_weight_kg: float) -> bool:
        """Проверяет, подходит ли транспорт по грузоподъёмности."""
        return self.is_available and 0 < cargo_weight_kg <= self.capacity_kg

    def change_location(self, new_location: str):
        """Изменяет местоположение транспортного средства."""
        if not new_location:
            raise InvalidVehicleError("Местоположение не может быть пустым.")
        self.current_location = new_location

    def calculate_age(self) -> int:
        """Возвращает возраст транспортного средства в годах."""
        return date.today().year - self.year

    def needs_inspection(self) -> bool:
        """Проверяет, есть ли хотя бы один непройденный техосмотр."""
        return any(not inspection.passed for inspection in self.inspections)

    def add_inspection(self, inspection):
        """Добавляет запись о техосмотре."""
        if inspection.vehicle is not self:
            raise InvalidVehicleError("Техосмотр относится к другому транспортному средству.")
        self.inspections.append(inspection)

    def add_maintenance_record(self, record):
        """Добавляет запись о техническом обслуживании."""
        if record.vehicle is not self:
            raise InvalidVehicleError(
                "Запись о ремонте относится к другому транспортному средству."
            )
        self.maintenance_records.append(record)

    def add_fuel_record(self, record):
        """Добавляет запись о заправке."""
        if record.vehicle is not self:
            raise InvalidVehicleError(
                "Запись о заправке относится к другому транспортному средству."
            )
        self.fuel_records.append(record)

    def calculate_total_fuel(self) -> float:
        """Считает общий объём топлива по всем записям."""
        return sum(record.liters for record in self.fuel_records)

    def calculate_total_maintenance_cost(self) -> float:
        """Считает общую стоимость обслуживания и ремонта."""
        return sum(record.cost for record in self.maintenance_records)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number}), {self.capacity_kg} кг"