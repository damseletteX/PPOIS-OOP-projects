from datetime import date
from .Vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
)


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