from .Employee import Employee


class Driver(Employee):
    """Водитель транспортной компании."""

    def __init__(
        self,
        name: str,
        phone: str,
        employee_id: str,
        salary: float,
        license_number: str,
        license_categories: list[str],
        experience_years: int,
        email: str = "",
    ):
        super().__init__(name, phone, employee_id, salary, email)
        if not license_number.strip():
            raise ValueError("Номер водительского удостоверения обязателен.")
        if experience_years < 0:
            raise ValueError("Стаж не может быть отрицательным.")
        if not license_categories:
            raise ValueError("Укажите хотя бы одну категорию прав.")

        self.license_number = license_number.strip()
        self.license_categories = set(license_categories)
        self.experience_years = experience_years
        self.assigned_vehicle = None
        self.completed_trips = 0
        self.is_on_trip = False

    def can_drive_category(self, category: str) -> bool:
        return category in self.license_categories

    def assign_vehicle(self, vehicle) -> None:
        if not self.is_ready_for_work():
            raise ValueError("Водитель сейчас недоступен.")
        if self.is_on_trip:
            raise ValueError("Водитель уже находится в рейсе.")
        if not getattr(vehicle, "is_available", False):
            raise ValueError("Транспортное средство недоступно.")

        required_category = getattr(vehicle, "required_license_category", None)
        if required_category and not self.can_drive_category(required_category):
            raise ValueError("У водителя нет нужной категории прав.")

        self.assigned_vehicle = vehicle

    def start_trip(self) -> None:
        if not self.is_ready_for_work():
            raise ValueError("Водитель не готов к работе.")
        if self.assigned_vehicle is None:
            raise ValueError("Сначала назначьте транспорт.")
        if self.is_on_trip:
            raise ValueError("Водитель уже находится в рейсе.")

        self.is_on_trip = True
        self.is_available = False
        self.assigned_vehicle.is_available = False

    def finish_trip(self) -> None:
        if not self.is_on_trip:
            raise ValueError("У водителя нет активного рейса.")

        self.is_on_trip = False
        self.is_available = True
        self.completed_trips += 1
        self.assigned_vehicle.is_available = True
        self.assigned_vehicle = None

    def is_experienced(self, minimum_years: int = 3) -> bool:
        return self.experience_years >= minimum_years

    def update_license_categories(self, categories: list[str]) -> None:
        if not categories:
            raise ValueError("Нужна хотя бы одна категория прав.")
        self.license_categories = set(categories)