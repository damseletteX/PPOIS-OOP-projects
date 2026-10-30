"""Классы транспортных средств и учёта их эксплуатации."""

from datetime import date

from .exceptions import (
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


class Truck(Vehicle):
    """Грузовой автомобиль."""

    def __init__(
        self,
        vehicle_id,
        brand,
        model,
        year,
        registration_number,
        capacity_kg,
        cargo_volume_m3,
        required_license_category="C",
        fuel_type="diesel",
    ):
        super().__init__(
            vehicle_id,
            brand,
            model,
            year,
            registration_number,
            capacity_kg,
            required_license_category,
            fuel_type,
        )
        if cargo_volume_m3 <= 0:
            raise InvalidVehicleError("Объём кузова должен быть положительным.")
        self.cargo_volume_m3 = cargo_volume_m3
        self.has_crane = False

    def install_crane(self):
        """Отмечает установку крана для погрузки."""
        self.has_crane = True

    def remove_crane(self):
        """Отмечает демонтаж крана."""
        self.has_crane = False

    def calculate_load_percentage(self, cargo_weight_kg: float) -> float:
        """Возвращает процент загрузки грузоподъёмности."""
        if not 0 <= cargo_weight_kg <= self.capacity_kg:
            raise InvalidVehicleError("Вес груза выходит за пределы грузоподъёмности.")
        return cargo_weight_kg / self.capacity_kg * 100


class Van(Vehicle):
    """Фургон для небольших грузов."""

    def __init__(
        self,
        vehicle_id,
        brand,
        model,
        year,
        registration_number,
        capacity_kg,
        cargo_volume_m3,
        required_license_category="B",
        fuel_type="diesel",
    ):
        super().__init__(
            vehicle_id,
            brand,
            model,
            year,
            registration_number,
            capacity_kg,
            required_license_category,
            fuel_type,
        )
        if cargo_volume_m3 <= 0:
            raise InvalidVehicleError("Объём фургона должен быть положительным.")
        self.cargo_volume_m3 = cargo_volume_m3
        self.has_side_door = True

    def open_side_door(self):
        """Проверяет наличие боковой двери и открывает её."""
        if not self.has_side_door:
            raise InvalidVehicleError("У фургона нет боковой двери.")
        return "Боковая дверь открыта."

    def remove_side_door(self):
        """Отмечает, что боковая дверь отсутствует."""
        self.has_side_door = False


class RefrigeratedTruck(Truck):
    """Грузовик с холодильной установкой."""

    def __init__(
        self,
        vehicle_id,
        brand,
        model,
        year,
        registration_number,
        capacity_kg,
        cargo_volume_m3,
        min_temperature_c,
        max_temperature_c,
        required_license_category="C",
        fuel_type="diesel",
    ):
        super().__init__(
            vehicle_id,
            brand,
            model,
            year,
            registration_number,
            capacity_kg,
            cargo_volume_m3,
            required_license_category,
            fuel_type,
        )
        if min_temperature_c > max_temperature_c:
            raise InvalidVehicleError("Минимальная температура выше максимальной.")
        self.min_temperature_c = min_temperature_c
        self.max_temperature_c = max_temperature_c
        self.current_temperature_c = 5.0
        self.cooling_enabled = False

    def set_temperature(self, temperature_c: float):
        """Устанавливает температуру внутри кузова."""
        if not self.min_temperature_c <= temperature_c <= self.max_temperature_c:
            raise InvalidVehicleError("Температура выходит за допустимый диапазон.")
        self.current_temperature_c = temperature_c

    def enable_cooling(self):
        """Включает холодильную установку."""
        self.cooling_enabled = True

    def disable_cooling(self):
        """Выключает холодильную установку."""
        self.cooling_enabled = False

    def check_temperature(self) -> bool:
        """Проверяет, соответствует ли текущая температура заданному диапазону."""
        return self.min_temperature_c <= self.current_temperature_c <= self.max_temperature_c


class Tanker(Vehicle):
    """Автоцистерна для жидких грузов."""

    def __init__(
        self,
        vehicle_id,
        brand,
        model,
        year,
        registration_number,
        capacity_kg,
        tank_volume_liters,
        required_license_category="C",
        fuel_type="diesel",
    ):
        super().__init__(
            vehicle_id,
            brand,
            model,
            year,
            registration_number,
            capacity_kg,
            required_license_category,
            fuel_type,
        )
        if tank_volume_liters <= 0:
            raise InvalidVehicleError("Объём цистерны должен быть положительным.")
        self.tank_volume_liters = tank_volume_liters
        self.current_volume_liters = 0.0
        self.tank_clean = True

    def load_liquid(self, volume_liters: float):
        """Загружает жидкость в цистерну."""
        if not self.tank_clean:
            raise InvalidVehicleError("Цистерна должна быть очищена перед загрузкой.")
        if volume_liters <= 0:
            raise InvalidVehicleError("Объём загрузки должен быть положительным.")
        if self.current_volume_liters + volume_liters > self.tank_volume_liters:
            raise InvalidVehicleError("Превышен объём цистерны.")
        self.current_volume_liters += volume_liters

    def unload_liquid(self, volume_liters: float):
        """Выгружает жидкость из цистерны."""
        if volume_liters <= 0 or volume_liters > self.current_volume_liters:
            raise InvalidVehicleError("Некорректный объём выгрузки.")
        self.current_volume_liters -= volume_liters

    def clean_tank(self):
        """Отмечает цистерну как очищенную."""
        if self.current_volume_liters > 0:
            raise InvalidVehicleError("Нельзя очистить заполненную цистерну.")
        self.tank_clean = True

    def mark_tank_dirty(self):
        """Отмечает, что цистерна нуждается в очистке."""
        self.tank_clean = False


class FlatbedTruck(Truck):
    """Грузовик с открытой платформой."""

    def __init__(
        self,
        vehicle_id,
        brand,
        model,
        year,
        registration_number,
        capacity_kg,
        cargo_volume_m3,
        platform_length_m,
        required_license_category="C",
        fuel_type="diesel",
    ):
        super().__init__(
            vehicle_id,
            brand,
            model,
            year,
            registration_number,
            capacity_kg,
            cargo_volume_m3,
            required_license_category,
            fuel_type,
        )
        if platform_length_m <= 0:
            raise InvalidVehicleError("Длина платформы должна быть положительной.")
        self.platform_length_m = platform_length_m
        self.cargo_secured = False

    def secure_cargo(self):
        """Отмечает, что груз закреплён на платформе."""
        self.cargo_secured = True

    def release_cargo(self):
        """Снимает отметку о закреплении груза."""
        self.cargo_secured = False

    def can_carry_length(self, cargo_length_m: float) -> bool:
        """Проверяет, помещается ли груз по длине платформы."""
        return 0 < cargo_length_m <= self.platform_length_m


class Trailer:
    """Прицеп, который может быть присоединён к тягачу."""

    def __init__(
        self,
        trailer_id: str,
        registration_number: str,
        capacity_kg: float,
        volume_m3: float,
    ):
        if not trailer_id or not registration_number:
            raise InvalidVehicleError("Укажите ID и номер прицепа.")
        if capacity_kg <= 0 or volume_m3 <= 0:
            raise InvalidVehicleError("Параметры прицепа должны быть положительными.")

        self.trailer_id = trailer_id
        self.registration_number = registration_number
        self.capacity_kg = capacity_kg
        self.volume_m3 = volume_m3
        self.is_attached = False
        self.attached_vehicle = None
        self.is_available = True

    def attach_to(self, vehicle: Vehicle):
        """Присоединяет прицеп к доступному тягачу."""
        if self.is_attached:
            raise InvalidVehicleError("Прицеп уже присоединён.")
        if not vehicle.is_available:
            raise VehicleUnavailableError("Тягач недоступен.")
        self.attached_vehicle = vehicle
        self.is_attached = True
        self.is_available = False

    def detach(self):
        """Отсоединяет прицеп от тягача."""
        if not self.is_attached:
            raise InvalidVehicleError("Прицеп не присоединён.")
        self.attached_vehicle = None
        self.is_attached = False
        self.is_available = True

    def can_carry(self, cargo_weight_kg: float) -> bool:
        """Проверяет, помещается ли груз по массе."""
        return 0 < cargo_weight_kg <= self.capacity_kg


class VehicleInspection:
    """Запись о техническом осмотре."""

    def __init__(
        self,
        inspection_id: str,
        vehicle: Vehicle,
        inspection_date: date,
        inspector: str,
    ):
        if not inspection_id or not inspector:
            raise InvalidVehicleError("Укажите ID осмотра и имя проверяющего.")
        self.inspection_id = inspection_id
        self.vehicle = vehicle
        self.inspection_date = inspection_date
        self.inspector = inspector
        self.passed = False
        self.notes = ""
        self.next_inspection_date = None

    def conduct(self, passed: bool, notes: str = ""):
        """Фиксирует результат технического осмотра."""
        self.passed = passed
        self.notes = notes
        if not passed:
            self.vehicle.is_available = False

    def schedule_next(self, next_date: date):
        """Назначает дату следующего осмотра."""
        if next_date <= self.inspection_date:
            raise InvalidVehicleError("Следующий осмотр должен быть назначен позже.")
        self.next_inspection_date = next_date

    def is_overdue(self, today: date | None = None) -> bool:
        """Проверяет, просрочен ли следующий осмотр."""
        today = today or date.today()
        return self.next_inspection_date is not None and today > self.next_inspection_date


class MaintenanceRecord:
    """Запись о ремонте или техническом обслуживании."""

    def __init__(
        self,
        record_id: str,
        vehicle: Vehicle,
        service_date: date,
        description: str,
        cost: float,
    ):
        if not record_id or not description:
            raise InvalidVehicleError("Укажите ID записи и описание работ.")
        if cost < 0:
            raise InvalidVehicleError("Стоимость работ не может быть отрицательной.")

        self.record_id = record_id
        self.vehicle = vehicle
        self.service_date = service_date
        self.description = description
        self.cost = cost
        self.completed = False
        self.parts_used = []
        self.odometer_km = vehicle.mileage_km

    def complete_service(self):
        """Отмечает ремонт или обслуживание как завершённое."""
        self.completed = True
        self.vehicle.mark_available()

    def add_part(self, part_name: str):
        """Добавляет использованную запчасть в запись."""
        if not part_name:
            raise InvalidVehicleError("Название запчасти не может быть пустым.")
        self.parts_used.append(part_name)

    def update_cost(self, new_cost: float):
        """Обновляет стоимость обслуживания."""
        if new_cost < 0:
            raise InvalidVehicleError("Стоимость не может быть отрицательной.")
        self.cost = new_cost


class FuelRecord:
    """Запись о заправке транспортного средства."""

    def __init__(
        self,
        record_id: str,
        vehicle: Vehicle,
        fuel_date: date,
        liters: float,
        price_per_liter: float,
    ):
        if not record_id:
            raise InvalidVehicleError("Укажите ID записи о заправке.")
        if liters <= 0 or price_per_liter < 0:
            raise InvalidVehicleError("Некорректный объём или цена топлива.")

        self.record_id = record_id
        self.vehicle = vehicle
        self.fuel_date = fuel_date
        self.liters = liters
        self.price_per_liter = price_per_liter
        self.total_cost = liters * price_per_liter
        self.fuel_type = vehicle.fuel_type
        self.odometer_km = vehicle.mileage_km

    def calculate_cost(self) -> float:
        """Возвращает полную стоимость заправки."""
        return self.liters * self.price_per_liter

    def update_price(self, new_price: float):
        """Пересчитывает стоимость при изменении цены за литр."""
        if new_price < 0:
            raise InvalidVehicleError("Цена топлива не может быть отрицательной.")
        self.price_per_liter = new_price
        self.total_cost = self.calculate_cost()
