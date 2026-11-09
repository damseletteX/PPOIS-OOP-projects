from ..exceptions import (
    InvalidCargoError,
)


class Cargo:
    """Базовый класс груза."""

    def __init__(
        self,
        cargo_id: str,
        name: str,
        weight_kg: float,
        volume_m3: float,
        declared_value: float = 0.0,
        description: str = "",
    ):
        if not cargo_id or not name:
            raise InvalidCargoError("ID и название груза обязательны.")
        if weight_kg <= 0 or volume_m3 <= 0:
            raise InvalidCargoError("Вес и объём груза должны быть положительными.")
        if declared_value < 0:
            raise InvalidCargoError("Стоимость груза не может быть отрицательной.")

        self.cargo_id = cargo_id
        self.name = name
        self.weight_kg = weight_kg
        self.volume_m3 = volume_m3
        self.declared_value = declared_value
        self.description = description
        self.is_packed = False
        self.is_insured = False
        self.status = "created"
        self.origin = ""
        self.destination = ""
        self.packages = []
        self.documents = []

    def set_destination(self, origin: str, destination: str):
        """Устанавливает пункты отправления и назначения."""
        if not origin or not destination:
            raise InvalidCargoError("Укажите отправление и назначение.")
        if origin == destination:
            raise InvalidCargoError("Пункты отправления и назначения совпадают.")
        self.origin = origin
        self.destination = destination

    def pack(self):
        """Отмечает груз как упакованный."""
        self.is_packed = True

    def unpack(self):
        """Снимает отметку об упаковке."""
        self.is_packed = False

    def mark_insured(self):
        """Отмечает груз как застрахованный."""
        self.is_insured = True

    def update_status(self, new_status: str):
        """Изменяет статус груза."""
        allowed_statuses = {"created", "packed", "in_transit", "delivered", "damaged"}
        if new_status not in allowed_statuses:
            raise InvalidCargoError("Неизвестный статус груза.")
        self.status = new_status
        if new_status == "packed":
            self.is_packed = True

    def calculate_density(self) -> float:
        """Вычисляет плотность груза в кг/м³."""
        return self.weight_kg / self.volume_m3

    def check_vehicle_capacity(self, vehicle) -> bool:
        """Проверяет, подходит ли транспорт по весу и объёму."""
        if self.weight_kg > vehicle.capacity_kg:
            return False

        vehicle_volume = getattr(vehicle, "cargo_volume_m3", None)
        if vehicle_volume is not None and self.volume_m3 > vehicle_volume:
            return False

        return not hasattr(vehicle, "tank_volume_liters")

    def add_package(self, package):
        """Добавляет упаковку к грузу."""
        if package in self.packages:
            raise InvalidCargoError("Эта упаковка уже добавлена.")
        self.packages.append(package)

    def add_document(self, document):
        """Добавляет сопроводительный документ."""
        if document in self.documents:
            raise InvalidCargoError("Этот документ уже добавлен.")
        if document.cargo is not self:
            raise InvalidCargoError("Документ относится к другому грузу.")
        self.documents.append(document)

    def calculate_total_packaging_weight(self) -> float:
        """Считает суммарный вес всех упаковок."""
        return sum(package.weight_kg for package in self.packages)

    def has_required_documents(self, required_types: list[str]) -> bool:
        """Проверяет наличие документов заданных типов."""
        available_types = {document.document_type for document in self.documents}
        return all(doc_type in available_types for doc_type in required_types)

    def __str__(self):
        return f"{self.name} ({self.weight_kg} кг, {self.volume_m3} м³)"
