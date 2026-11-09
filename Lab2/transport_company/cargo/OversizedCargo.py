from ..exceptions import (  # noqa: N999
    InvalidCargoError,
)
from .Cargo import Cargo


class OversizedCargo(Cargo):
    """Негабаритный груз."""

    def __init__(
        self,
        cargo_id,
        name,
        weight_kg,
        volume_m3,
        length_m: float,
        width_m: float,
        height_m: float,
        declared_value=0.0,
        description="",
    ):
        super().__init__(cargo_id, name, weight_kg, volume_m3, declared_value, description)
        if min(length_m, width_m, height_m) <= 0:
            raise InvalidCargoError("Габариты должны быть положительными.")

        self.length_m = length_m
        self.width_m = width_m
        self.height_m = height_m
        self.requires_special_permit = True
        self.permit_number = ""
        self.route_restrictions = []
        self.requires_escort = False

    def calculate_geometric_volume(self) -> float:
        """Вычисляет объём по длине, ширине и высоте."""
        return self.length_m * self.width_m * self.height_m

    def set_permit(self, permit_number: str):
        """Указывает разрешение на перевозку негабаритного груза."""
        if not permit_number:
            raise InvalidCargoError("Номер разрешения не может быть пустым.")
        self.permit_number = permit_number

    def add_route_restriction(self, restriction: str):
        """Добавляет ограничение маршрута."""
        if not restriction:
            raise InvalidCargoError("Ограничение не может быть пустым.")
        self.route_restrictions.append(restriction)

    def require_escort(self):
        """Отмечает необходимость сопровождения."""
        self.requires_escort = True

    def check_flatbed(self, vehicle) -> bool:
        """Проверяет, подходит ли открытая платформа по длине."""
        return (
            hasattr(vehicle, "platform_length_m")
            and vehicle.can_carry_length(self.length_m)
            and vehicle.capacity_kg >= self.weight_kg
        )