from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    CURRENCY_DIGITS,
    DONATION_VALUE_RATE,
    FIELD_AMOUNT,
    FIELD_ID,
)
from ..validation import require_non_negative, require_text

if TYPE_CHECKING:
    from ..catalog.item_copy import ItemCopy
    from ..people.reader import Reader
    from ..people.staff import Staff


class Donation:
    """Пожертвование книг или денег библиотеке."""

    def __init__(
        self,
        donation_id: str,
        donor: Reader | None,
        received_on: date,
        cash_amount: float = 0.0,
    ):
        self.donation_id = require_text(donation_id, FIELD_ID)
        self.donor = donor
        self.received_on = received_on
        self.cash_amount = require_non_negative(cash_amount, FIELD_AMOUNT)
        self.copies: list[ItemCopy] = []
        self.accepted_by: Staff | None = None

    def add_copy(self, copy: ItemCopy) -> None:
        """Добавляет подаренный экземпляр."""
        self.copies.append(copy)

    def item_count(self) -> int:
        """Возвращает число подаренных экземпляров."""
        return len(self.copies)

    def estimated_value(self) -> float:
        """Оценивает стоимость: деньги плюс часть цены книг."""
        books_value = sum(copy.price for copy in self.copies) * DONATION_VALUE_RATE
        return round(self.cash_amount + books_value, CURRENCY_DIGITS)

    def is_monetary(self) -> bool:
        """Проверяет, что в пожертвование входят деньги."""
        return self.cash_amount > 0

    def accept(self, staff: Staff) -> None:
        """Фиксирует сотрудника, принявшего пожертвование."""
        self.accepted_by = staff

    def is_anonymous(self) -> bool:
        """Проверяет, что даритель не указан."""
        return self.donor is None
