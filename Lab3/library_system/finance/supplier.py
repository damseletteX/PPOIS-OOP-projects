from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import (
    FIELD_DAYS,
    FIELD_ID,
    FIELD_NAME,
    FIELD_PHONE,
    FIELD_RATING,
    MAX_RATING,
    MIN_RATING,
    RELIABLE_SUPPLIER_RATING,
)
from ..validation import require_in_range, require_positive, require_text

if TYPE_CHECKING:
    from .purchase_order import PurchaseOrder


class Supplier:
    """Поставщик изданий."""

    def __init__(self, supplier_id: str, name: str, phone: str, delivery_days: int):
        self.supplier_id = require_text(supplier_id, FIELD_ID)
        self.name = require_text(name, FIELD_NAME)
        self.phone = require_text(phone, FIELD_PHONE)
        self.delivery_days = require_positive(delivery_days, FIELD_DAYS)
        self.ratings: list[int] = []
        self.orders: list[PurchaseOrder] = []

    def add_order(self, order: PurchaseOrder) -> None:
        """Добавляет заказ в историю поставщика."""
        self.orders.append(order)

    def rate(self, score: int) -> None:
        """Добавляет оценку качества поставки."""
        self.ratings.append(require_in_range(score, MIN_RATING, MAX_RATING, FIELD_RATING))

    def average_rating(self) -> float:
        """Возвращает среднюю оценку поставщика."""
        return round(sum(self.ratings) / len(self.ratings), 1) if self.ratings else 0.0

    def is_reliable(self) -> bool:
        """Проверяет, что оценка поставщика достаточно высока."""
        return self.average_rating() >= RELIABLE_SUPPLIER_RATING

    def expected_delivery(self, on_date: date) -> date:
        """Возвращает ожидаемую дату поставки при заказе в указанный день."""
        return on_date + timedelta(days=self.delivery_days)

    def total_ordered(self) -> float:
        """Возвращает общую стоимость всех заказов."""
        return sum(order.total_cost() for order in self.orders)
