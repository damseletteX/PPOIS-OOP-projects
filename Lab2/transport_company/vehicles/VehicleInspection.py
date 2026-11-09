from datetime import date
from .Vehicle import Vehicle
from ..exceptions import (
    InvalidVehicleError,
)


class VehicleInspection:
    """Запись о техническом осмотре."""

    def __init__(
        self,
        inspection_id: str,
        vehicle: Vehicle,
        inspection_date: date,
        inspector: str,
    ):
        if not inspection_id or not inspector:
            raise InvalidVehicleError("Укажите ID осмотра и имя проверяющего.")
        self.inspection_id = inspection_id
        self.vehicle = vehicle
        self.inspection_date = inspection_date
        self.inspector = inspector
        self.passed = False
        self.notes = ""
        self.next_inspection_date = None

    def conduct(self, passed: bool, notes: str = ""):
        """Фиксирует результат технического осмотра."""
        self.passed = passed
        self.notes = notes
        if not passed:
            self.vehicle.is_available = False

    def schedule_next(self, next_date: date):
        """Назначает дату следующего осмотра."""
        if next_date <= self.inspection_date:
            raise InvalidVehicleError("Следующий осмотр должен быть назначен позже.")
        self.next_inspection_date = next_date

    def is_overdue(self, today: date | None = None) -> bool:
        """Проверяет, просрочен ли следующий осмотр."""
        today = today or date.today()
        return self.next_inspection_date is not None and today > self.next_inspection_date