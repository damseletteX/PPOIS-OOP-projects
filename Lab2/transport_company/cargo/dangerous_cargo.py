from ..exceptions import (
    InvalidCargoError,
)
from .cargo import Cargo


class DangerousCargo(Cargo):
    """Опасный груз."""

    def __init__(
        self,
        cargo_id,
        name,
        weight_kg,
        volume_m3,
        hazard_class: str,
        un_number: str,
        declared_value=0.0,
        description="",
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
