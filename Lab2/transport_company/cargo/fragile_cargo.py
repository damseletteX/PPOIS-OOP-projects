from ..exceptions import (
    InvalidCargoError,
)
from .cargo import Cargo


class FragileCargo(Cargo):
    """Хрупкий груз."""

    def __init__(
        self,
        cargo_id,
        name,
        weight_kg,
        volume_m3,
        fragility_level: int = 3,
        declared_value=0.0,
        description="",
    ):
        super().__init__(cargo_id, name, weight_kg, volume_m3, declared_value, description)
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