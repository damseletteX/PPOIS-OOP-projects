from .Employee import Employee


class Dispatcher(Employee):
    """Диспетчер, координирующий перевозки."""

    def __init__(self, name: str, phone: str, employee_id: str, salary: float, email: str = ""):
        super().__init__(name, phone, employee_id, salary, email)
        self.managed_trips = []
        self.shift = "day"
        self.max_trips = 20

    def register_trip(self, trip) -> None:
        if not self.is_active:
            raise ValueError("Неактивный диспетчер не может вести рейсы.")
        if trip in self.managed_trips:
            raise ValueError("Этот рейс уже зарегистрирован.")
        if len(self.managed_trips) >= self.max_trips:
            raise ValueError("Диспетчер достиг лимита рейсов.")
        self.managed_trips.append(trip)

    def close_trip(self, trip) -> None:
        if trip not in self.managed_trips:
            raise ValueError("Рейс не закреплён за диспетчером.")
        self.managed_trips.remove(trip)

    def set_shift(self, shift: str) -> None:
        if shift not in ("day", "night"):
            raise ValueError("Смена должна быть day или night.")
        self.shift = shift

    def find_managed_trip(self, trip_id: str):
        for trip in self.managed_trips:
            if getattr(trip, "trip_id", None) == trip_id:
                return trip
        return None

    def has_free_capacity(self) -> bool:
        return len(self.managed_trips) < self.max_trips