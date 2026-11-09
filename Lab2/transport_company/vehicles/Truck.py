from .Vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
)


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