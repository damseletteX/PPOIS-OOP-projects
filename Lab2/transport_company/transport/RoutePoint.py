from datetime import datetime
from ..exceptions import (
    InvalidRouteError,
)


class RoutePoint:
    """Отдельная точка маршрута."""

    def __init__(
        self,
        point_id: str,
        address: str,
        sequence_number: int,
        planned_arrival: datetime | None = None,
    ):
        if not point_id or not address:
            raise InvalidRouteError("ID точки и адрес обязательны.")
        if sequence_number < 1:
            raise InvalidRouteError("Номер точки должен быть положительным.")

        self.point_id = point_id
        self.address = address
        self.sequence_number = sequence_number
        self.planned_arrival = planned_arrival
        self.actual_arrival = None
        self.is_completed = False
        self.notes = ""

    def record_arrival(self, arrival_time: datetime | None = None):
        """Фиксирует фактическое прибытие в точку."""
        self.actual_arrival = arrival_time or datetime.now()
        self.is_completed = True

    def set_planned_arrival(self, arrival_time: datetime):
        """Устанавливает плановое время прибытия."""
        self.planned_arrival = arrival_time

    def delay_minutes(self) -> int:
        """Вычисляет задержку относительно планового прибытия."""
        if self.planned_arrival is None or self.actual_arrival is None:
            return 0
        delay = self.actual_arrival - self.planned_arrival
        return max(0, int(delay.total_seconds() // 60))

    def add_note(self, note: str):
        """Добавляет примечание к точке маршрута."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()