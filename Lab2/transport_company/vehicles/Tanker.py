from .Vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
)


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