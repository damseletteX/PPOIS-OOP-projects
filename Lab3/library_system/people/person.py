from __future__ import annotations

from datetime import date

from ..constants import ADULT_AGE, FIELD_EMAIL, FIELD_NAME, FIELD_PHONE
from ..validation import require_email, require_text


class Person:
    """Базовый класс человека: читатель или сотрудник."""

    def __init__(self, name: str, phone: str, birth_date: date, email: str = ""):
        self.name = require_text(name, FIELD_NAME)
        self.phone = require_text(phone, FIELD_PHONE)
        self.email = require_email(email, FIELD_EMAIL)
        self.birth_date = birth_date
        self.is_active = True

    def update_phone(self, phone: str) -> None:
        """Меняет номер телефона."""
        self.phone = require_text(phone, FIELD_PHONE)

    def update_email(self, email: str) -> None:
        """Меняет адрес электронной почты."""
        self.email = require_email(email, FIELD_EMAIL)

    def age_on(self, on_date: date) -> int:
        """Возвращает полное число лет на указанную дату."""
        had_birthday = (on_date.month, on_date.day) >= (self.birth_date.month, self.birth_date.day)
        return on_date.year - self.birth_date.year - (0 if had_birthday else 1)

    def is_adult_on(self, on_date: date) -> bool:
        """Проверяет, что человек совершеннолетний на указанную дату."""
        return self.age_on(on_date) >= ADULT_AGE

    def deactivate(self) -> None:
        """Делает человека неактивным."""
        self.is_active = False

    def activate(self) -> None:
        """Возвращает человека в число активных."""
        self.is_active = True

    def contact_information(self) -> str:
        """Возвращает контактные данные одной строкой."""
        return f"{self.name}, телефон: {self.phone}, email: {self.email or '—'}"
