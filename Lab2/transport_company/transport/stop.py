from datetime import datetime
from ..exceptions import (
    InvalidRouteError,
)


class Stop:
    """Остановка во время рейса."""

    def __init__(
        self,
        stop_id: str,
        address: str,
        purpose: str = "other",
    ):
        if not stop_id or not address:
            raise InvalidRouteError("ID остановки и адрес обязательны.")
        if purpose not in {"loading", "unloading", "rest", "fuel", "other"}:
            raise InvalidRouteError("Неизвестная цель остановки.")

        self.stop_id = stop_id
        self.address = address
        self.purpose = purpose
        self.planned_time = None
        self.actual_time = None
        self.duration_minutes = 0
        self.is_completed = False
        self.notes = ""

    def schedule(self, planned_time: datetime, duration_minutes: int = 0):
        """Назначает время и длительность остановки."""
        if duration_minutes < 0:
            raise InvalidRouteError("Длительность не может быть отрицательной.")
        self.planned_time = planned_time
        self.duration_minutes = duration_minutes

    def complete(self, actual_time: datetime | None = None):
        """Отмечает остановку как завершённую."""
        self.actual_time = actual_time or datetime.now()
        self.is_completed = True

    def delay_minutes(self) -> int:
        """Вычисляет задержку начала остановки."""
        if self.planned_time is None or self.actual_time is None:
            return 0
        delay = self.actual_time - self.planned_time
        return max(0, int(delay.total_seconds() // 60))

    def add_note(self, note: str):
        """Добавляет примечание к остановке."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()