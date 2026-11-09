from .RoutePoint import RoutePoint
from ..exceptions import (
    InvalidRouteError,
)


class Route:
    """Маршрут перевозки."""

    def __init__(
        self,
        route_id: str,
        name: str,
        origin: str,
        destination: str,
        distance_km: float,
    ):
        if not route_id or not name or not origin or not destination:
            raise InvalidRouteError("Заполните основные данные маршрута.")
        if origin == destination:
            raise InvalidRouteError("Начало и конец маршрута совпадают.")
        if distance_km <= 0:
            raise InvalidRouteError("Длина маршрута должна быть положительной.")

        self.route_id = route_id
        self.name = name
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.points = []
        self.is_active = True
        self.estimated_duration_hours = 0.0
        self.restrictions = []
        self.toll_cost = 0.0

    def add_point(self, point: RoutePoint):
        """Добавляет промежуточную точку маршрута."""
        if any(p.point_id == point.point_id for p in self.points):
            raise InvalidRouteError("Такая точка уже есть в маршруте.")
        if any(p.sequence_number == point.sequence_number for p in self.points):
            raise InvalidRouteError("Номер точки уже используется.")
        self.points.append(point)
        self.points.sort(key=lambda p: p.sequence_number)

    def remove_point(self, point_id: str) -> bool:
        """Удаляет точку маршрута по ID."""
        for point in self.points:
            if point.point_id == point_id:
                self.points.remove(point)
                return True
        return False

    def calculate_duration(self, average_speed_kmh: float) -> float:
        """Оценивает время движения без учёта остановок."""
        if average_speed_kmh <= 0:
            raise InvalidRouteError("Средняя скорость должна быть положительной.")
        self.estimated_duration_hours = self.distance_km / average_speed_kmh
        return self.estimated_duration_hours

    def calculate_cost(self, cost_per_km: float) -> float:
        """Вычисляет стоимость маршрута по цене за километр."""
        if cost_per_km < 0:
            raise InvalidRouteError("Цена за километр не может быть отрицательной.")
        return self.distance_km * cost_per_km + self.toll_cost

    def add_restriction(self, restriction: str):
        """Добавляет ограничение маршрута."""
        if not restriction:
            raise InvalidRouteError("Ограничение не может быть пустым.")
        self.restrictions.append(restriction)

    def set_active(self, active: bool):
        """Включает или отключает маршрут."""
        self.is_active = active

    def get_next_point(self) -> RoutePoint | None:
        """Возвращает ближайшую незавершённую точку."""
        for point in self.points:
            if not point.is_completed:
                return point
        return None

    def progress_percentage(self) -> float:
        """Вычисляет долю пройденных промежуточных точек."""
        if not self.points:
            return 100.0
        completed = sum(point.is_completed for point in self.points)
        return completed / len(self.points) * 100