from datetime import date

from ..exceptions import (
    InvalidCargoError,
)


class CargoPackage:
    """Отдельная упаковка груза."""

    def __init__(
        self,
        package_id: str,
        package_type: str,
        weight_kg: float,
        label: str = "",
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