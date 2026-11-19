from datetime import date  # noqa: I001, N999
from .cargo import Cargo
from ..exceptions import (
    InvalidCargoError,
)


class PerishableCargo(Cargo):
    """Скоропортящийся груз."""

    def __init__(
        self,
        cargo_id,
        name,
        weight_kg,
        volume_m3,
        expiry_date: date,
        storage_temperature_c: float,
        declared_value=0.0,
        description="",
    ):
        super().__init__(
            cargo_id, name, weight_kg, volume_m3, declared_value, description
        )
        if expiry_date < date.today():
            raise InvalidCargoError("Срок годности груза уже истёк.")

        self.expiry_date = expiry_date
        self.storage_temperature_c = storage_temperature_c
        self.requires_refrigeration = True
        self.temperature_history = []

    def is_expired(self, today: date | None = None) -> bool:
        """Проверяет, истёк ли срок годности."""
        today = today or date.today()
        return today > self.expiry_date

    def record_temperature(self, temperature_c: float):
        """Добавляет показание температуры хранения."""
        self.temperature_history.append(temperature_c)

    def check_storage_temperature(self, temperature_c: float) -> bool:
        """Проверяет соответствие заданной температуры хранения."""
        return temperature_c == self.storage_temperature_c

    def check_refrigerated_vehicle(self, vehicle) -> bool:
        """Проверяет, подходит ли холодильный транспорт."""
        return (
            getattr(vehicle, "cooling_enabled", False)
            and vehicle.min_temperature_c
            <= self.storage_temperature_c
            <= vehicle.max_temperature_c
        )

    def days_until_expiry(self, today: date | None = None) -> int:
        """Возвращает количество дней до истечения срока годности."""
        today = today or date.today()
        return (self.expiry_date - today).days
