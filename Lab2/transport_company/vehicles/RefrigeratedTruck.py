from .Truck import Truck
from ..exceptions import (
    InvalidVehicleError,
)


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