from .vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
)


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