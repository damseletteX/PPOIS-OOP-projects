
"""Классы грузов, упаковок и сопроводительных документов."""

from datetime import date

from exceptions import (
    InvalidCargoError,
    CargoCapacityExceededError,
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
        allowed_statuses = {
            "created", "packed", "in_transit", "delivered", "damaged"
        }
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

        if hasattr(vehicle, "tank_volume_liters"):
            return False

        return True

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


class PerishableCargo(Cargo):
    """Скоропортящийся груз."""

    def __init__(
        self, cargo_id, name, weight_kg, volume_m3,
        expiry_date: date, storage_temperature_c: float,
        declared_value=0.0, description="",
    ):
        super().__init__(
            cargo_id, name, weight_kg, volume_m3, declared_value, description
        )
        if expiry_date < date.today():
            raise InvalidCargoError("Срок годности груза уже истёк.")

        self.expiry_date = expiry_date
        self.storage_temperature_c = storage_temperature_c
        self.requires_refrigeration = True
        self.temperature_history = []

    def is_expired(self, today: date | None = None) -> bool:
        """Проверяет, истёк ли срок годности."""
        today = today or date.today()
        return today > self.expiry_date

    def record_temperature(self, temperature_c: float):
        """Добавляет показание температуры хранения."""
        self.temperature_history.append(temperature_c)

    def check_storage_temperature(self, temperature_c: float) -> bool:
        """Проверяет соответствие заданной температуры хранения."""
        return temperature_c == self.storage_temperature_c

    def check_refrigerated_vehicle(self, vehicle) -> bool:
        """Проверяет, подходит ли холодильный транспорт."""
        return (
            getattr(vehicle, "cooling_enabled", False)
            and vehicle.min_temperature_c <= self.storage_temperature_c
            <= vehicle.max_temperature_c
        )

    def days_until_expiry(self, today: date | None = None) -> int:
        """Возвращает количество дней до истечения срока годности."""
        today = today or date.today()
        return (self.expiry_date - today).days


class FragileCargo(Cargo):
    """Хрупкий груз."""

    def __init__(
        self, cargo_id, name, weight_kg, volume_m3,
        fragility_level: int = 3, declared_value=0.0, description="",
    ):
        super().__init__(
            cargo_id, name, weight_kg, volume_m3, declared_value, description
        )
        if not 1 <= fragility_level <= 5:
            raise InvalidCargoError("Уровень хрупкости должен быть от 1 до 5.")

        self.fragility_level = fragility_level
        self.requires_special_handling = True
        self.shock_sensitive = True
        self.handling_instructions = "Обращаться осторожно"

    def set_handling_instructions(self, instructions: str):
        """Устанавливает инструкции по обращению с грузом."""
        if not instructions:
            raise InvalidCargoError("Инструкция не может быть пустой.")
        self.handling_instructions = instructions

    def assess_damage_risk(self, handling_quality: int) -> str:
        """Оценивает риск повреждения по качеству обращения от 1 до 5."""
        if not 1 <= handling_quality <= 5:
            raise InvalidCargoError("Качество обращения должно быть от 1 до 5.")

        risk = self.fragility_level / handling_quality
        if risk >= 1:
            return "high"
        if risk >= 0.5:
            return "medium"
        return "low"

    def requires_careful_loading(self) -> bool:
        """Определяет, нужна ли осторожная погрузка."""
        return self.fragility_level >= 3


class DangerousCargo(Cargo):
    """Опасный груз."""

    def __init__(
        self, cargo_id, name, weight_kg, volume_m3,
        hazard_class: str, un_number: str,
        declared_value=0.0, description="",
    ):
        super().__init__(
            cargo_id, name, weight_kg, volume_m3, declared_value, description
        )
        if not hazard_class or not un_number:
            raise InvalidCargoError("Укажите класс опасности и номер ООН.")

        self.hazard_class = hazard_class
        self.un_number = un_number
        self.requires_special_permit = True
        self.permit_number = ""
        self.emergency_contact = ""
        self.safety_instructions = []

    def set_permit(self, permit_number: str):
        """Указывает разрешение на перевозку опасного груза."""
        if not permit_number:
            raise InvalidCargoError("Номер разрешения не может быть пустым.")
        self.permit_number = permit_number

    def has_valid_permit(self) -> bool:
        """Проверяет, указан ли номер разрешения."""
        return bool(self.permit_number)

    def set_emergency_contact(self, contact: str):
        """Устанавливает контакт для чрезвычайных ситуаций."""
        if not contact:
            raise InvalidCargoError("Контакт не может быть пустым.")
        self.emergency_contact = contact

    def add_safety_instruction(self, instruction: str):
        """Добавляет правило безопасности."""
        if not instruction:
            raise InvalidCargoError("Правило безопасности не может быть пустым.")
        self.safety_instructions.append(instruction)

    def check_transport_requirements(self) -> bool:
        """Проверяет наличие разрешения и инструкций по безопасности."""
        return bool(self.permit_number and self.safety_instructions)


class OversizedCargo(Cargo):
    """Негабаритный груз."""

    def __init__(
        self, cargo_id, name, weight_kg, volume_m3,
        length_m: float, width_m: float, height_m: float,
        declared_value=0.0, description="",
    ):
        super().__init__(
            cargo_id, name, weight_kg, volume_m3, declared_value, description
        )
        if min(length_m, width_m, height_m) <= 0:
            raise InvalidCargoError("Габариты должны быть положительными.")

        self.length_m = length_m
        self.width_m = width_m
        self.height_m = height_m
        self.requires_special_permit = True
        self.permit_number = ""
        self.route_restrictions = []
        self.requires_escort = False

    def calculate_geometric_volume(self) -> float:
        """Вычисляет объём по длине, ширине и высоте."""
        return self.length_m * self.width_m * self.height_m

    def set_permit(self, permit_number: str):
        """Указывает разрешение на перевозку негабаритного груза."""
        if not permit_number:
            raise InvalidCargoError("Номер разрешения не может быть пустым.")
        self.permit_number = permit_number

    def add_route_restriction(self, restriction: str):
        """Добавляет ограничение маршрута."""
        if not restriction:
            raise InvalidCargoError("Ограничение не может быть пустым.")
        self.route_restrictions.append(restriction)

    def require_escort(self):
        """Отмечает необходимость сопровождения."""
        self.requires_escort = True

    def check_flatbed(self, vehicle) -> bool:
        """Проверяет, подходит ли открытая платформа по длине."""
        return (
            hasattr(vehicle, "platform_length_m")
            and vehicle.can_carry_length(self.length_m)
            and vehicle.capacity_kg >= self.weight_kg
        )


class CargoPackage:
    """Отдельная упаковка груза."""

    def __init__(
        self, package_id: str, package_type: str,
        weight_kg: float, label: str = "",
    ):
        if not package_id or not package_type:
            raise InvalidCargoError("Укажите ID и тип упаковки.")
        if weight_kg < 0:
            raise InvalidCargoError("Вес упаковки не может быть отрицательным.")

        self.package_id = package_id
        self.package_type = package_type
        self.weight_kg = weight_kg
        self.label = label
        self.is_sealed = False
        self.is_damaged = False
        self.contents_description = ""
        self.packing_date = None

    def seal(self):
        """Запечатывает упаковку."""
        if self.is_damaged:
            raise InvalidCargoError("Повреждённую упаковку нельзя запечатать.")
        self.is_sealed = True
        self.packing_date = date.today()

    def unseal(self):
        """Открывает упаковку."""
        self.is_sealed = False

    def mark_damaged(self, description: str = ""):
        """Отмечает упаковку как повреждённую."""
        self.is_damaged = True
        self.is_sealed = False
        self.contents_description = description

    def replace_label(self, new_label: str):
        """Заменяет маркировку упаковки."""
        if not new_label:
            raise InvalidCargoError("Маркировка не может быть пустой.")
        self.label = new_label

    def is_ready_for_transport(self) -> bool:
        """Проверяет готовность упаковки к перевозке."""
        return self.is_sealed and not self.is_damaged


class CargoDocument:
    """Сопроводительный документ на груз."""

    def __init__(
        self, document_id: str, cargo: Cargo,
        document_type: str, issue_date: date,
        issuer: str, expiry_date: date | None = None,
    ):
        if not document_id or not document_type or not issuer:
            raise InvalidCargoError(
                "ID, тип документа и организация-выдаватель обязательны."
            )
        if expiry_date is not None and expiry_date < issue_date:
            raise InvalidCargoError("Документ не может истекать до выдачи.")

        self.document_id = document_id
        self.cargo = cargo
        self.document_type = document_type
        self.issue_date = issue_date
        self.issuer = issuer
        self.expiry_date = expiry_date
        self.document_number = ""
        self.is_verified = False
        self.notes = ""

    def verify(self):
        """Отмечает документ как проверенный."""
        self.is_verified = True

    def revoke_verification(self):
        """Отменяет отметку о проверке."""
        self.is_verified = False

    def is_expired(self, today: date | None = None) -> bool:
        """Проверяет, истёк ли срок действия документа."""
        today = today or date.today()
        return self.expiry_date is not None and today > self.expiry_date

    def update_number(self, document_number: str):
        """Устанавливает номер документа."""
        if not document_number:
            raise InvalidCargoError("Номер документа не может быть пустым.")
        self.document_number = document_number

    def add_note(self, note: str):
        """Добавляет примечание к документу."""
        if not note:
            raise InvalidCargoError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()
