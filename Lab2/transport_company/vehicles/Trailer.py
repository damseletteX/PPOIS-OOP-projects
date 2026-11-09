from .Vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
    VehicleUnavailableError,
)


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