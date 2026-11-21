from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import CURRENCY_DIGITS, FIELD_PRICE, FIELD_QUANTITY, RULE_RECEIVE_QUANTITY
from ..exceptions import ValidationError
from ..validation import require_non_negative, require_positive

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem


class PurchaseLine:
    """Позиция заказа: издание, количество и цена."""

    def __init__(self, item: LibraryItem, quantity: int, unit_price: float):
        self.item = item
        self.quantity = require_positive(quantity, FIELD_QUANTITY)
        self.unit_price = require_non_negative(unit_price, FIELD_PRICE)
        self.received_quantity = 0

    def total(self) -> float:
        """Возвращает стоимость позиции."""
        return round(self.quantity * self.unit_price, CURRENCY_DIGITS)

    def remaining(self) -> int:
        """Возвращает число неполученных экземпляров."""
        return self.quantity - self.received_quantity

    def is_fully_received(self) -> bool:
        """Проверяет, что позиция получена полностью."""
        return self.remaining() == 0

    def receive(self, quantity: int) -> None:
        """Принимает часть или всю позицию."""
        require_positive(quantity, FIELD_QUANTITY)
        if quantity > self.remaining():
            raise ValidationError(FIELD_QUANTITY, RULE_RECEIVE_QUANTITY)
        self.received_quantity += quantity
