from datetime import date
from .Vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
)


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