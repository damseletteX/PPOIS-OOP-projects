from datetime import date
from .trip import Trip
from ..exceptions import (
    InvalidRouteError,
)


class Schedule:
    """Расписание рейсов."""

    def __init__(self, schedule_id: str, name: str):
        if not schedule_id or not name:
            raise InvalidRouteError("ID и название расписания обязательны.")

        self.schedule_id = schedule_id
        self.name = name
        self.trips = []
        self.is_active = True
        self.created_at = date.today()
        self.notes = ""

    def add_trip(self, trip: Trip):
        """Добавляет рейс, если время и ресурсы не конфликтуют."""
        if not self.is_active:
            raise InvalidRouteError("Расписание неактивно.")
        if any(existing.trip_id == trip.trip_id for existing in self.trips):
            raise InvalidRouteError("Этот рейс уже есть в расписании.")

        for existing in self.trips:
            if existing.status in {"completed", "cancelled"}:
                continue
            if existing.driver is trip.driver or existing.vehicle is trip.vehicle:
                if existing.departure_time == trip.departure_time:
                    raise InvalidRouteError("В это время водитель или транспорт уже назначен.")

        self.trips.append(trip)
        self.trips.sort(key=lambda item: item.departure_time)

    def remove_trip(self, trip_id: str) -> bool:
        """Удаляет запланированный рейс из расписания."""
        for trip in self.trips:
            if trip.trip_id == trip_id:
                if trip.status != "planned":
                    raise InvalidRouteError("Можно удалить только ещё не начатый рейс.")
                self.trips.remove(trip)
                return True
        return False

    def get_trips_for_date(self, target_date: date) -> list[Trip]:
        """Возвращает рейсы, назначенные на выбранную дату."""
        return [trip for trip in self.trips if trip.departure_time.date() == target_date]

    def get_available_trips(self) -> list[Trip]:
        """Возвращает рейсы, которые ещё не начались."""
        return [trip for trip in self.trips if trip.status == "planned"]

    def cancel_schedule(self):
        """Отключает расписание и отменяет запланированные рейсы."""
        self.is_active = False
        for trip in self.trips:
            if trip.status == "planned":
                trip.cancel("Расписание отменено")

    def add_note(self, note: str):
        """Добавляет примечание к расписанию."""
        if not note:
            raise InvalidRouteError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()