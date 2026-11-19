from .truck import Truck
from ..exceptions import (
    InvalidVehicleError,
)


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