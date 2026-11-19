from ..cargo.cargo import Cargo
from ..exceptions import (
    InvalidCargoError,
    DeliveryError,
)


class OrderItem:
    """Позиция транспортного заказа."""

    def __init__(
        self,
        item_id: str,
        cargo: Cargo,
        quantity: int = 1,
    ):
        if not item_id:
            raise InvalidCargoError("ID позиции заказа обязателен.")
        if quantity < 1:
            raise InvalidCargoError("Количество должно быть не меньше единицы.")

        self.item_id = item_id
        self.cargo = cargo
        self.quantity = quantity
        self.unit_price = 0.0
        self.special_instructions = ""
        self.is_loaded = False
        self.is_unloaded = False

    def total_weight(self) -> float:
        """Возвращает общий вес груза в позиции."""
        return self.cargo.weight_kg * self.quantity

    def total_volume(self) -> float:
        """Возвращает общий объём груза в позиции."""
        return self.cargo.volume_m3 * self.quantity

    def calculate_price(self) -> float:
        """Рассчитывает стоимость позиции."""
        return self.unit_price * self.quantity

    def set_unit_price(self, price: float):
        """Устанавливает цену за одну единицу груза."""
        if price < 0:
            raise InvalidCargoError("Цена не может быть отрицательной.")
        self.unit_price = price

    def set_instructions(self, instructions: str):
        """Устанавливает особые инструкции для перевозки."""
        self.special_instructions = instructions

    def mark_loaded(self):
        """Отмечает позицию как загруженную."""
        self.is_loaded = True
        self.is_unloaded = False

    def mark_unloaded(self):
        """Отмечает позицию как выгруженную."""
        if not self.is_loaded:
            raise DeliveryError("Нельзя выгрузить незагруженный груз.")
        self.is_unloaded = True