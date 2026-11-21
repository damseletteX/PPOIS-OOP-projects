from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    CHILD_LOAN_LIMIT,
    FIELD_AGE,
    FIELD_NAME,
    REASON_NO_CONSENT,
    RULE_ADULT,
)
from ..exceptions import ReaderBlockedError, ValidationError
from ..validation import require_text
from .reader import Reader

if TYPE_CHECKING:
    from ..catalog.library_item import LibraryItem


class ChildReader(Reader):
    """Читатель-ребёнок, действующий с согласия опекуна."""

    def __init__(
        self,
        reader_id: str,
        name: str,
        phone: str,
        birth_date: date,
        registered_on: date,
        guardian: Reader,
        school: str,
        email: str = "",
    ):
        super().__init__(reader_id, name, phone, birth_date, registered_on, email)
        self.guardian = guardian
        self.school = require_text(school, FIELD_NAME)
        self.guardian_consent = False

    def loan_limit(self) -> int:
        """Ребёнку выдаётся не больше установленного числа изданий."""
        return min(super().loan_limit(), CHILD_LOAN_LIMIT)

    def ensure_may_read(self, item: LibraryItem, on_date: date) -> None:
        """Кроме возраста, требуется согласие опекуна."""
        if not self.guardian_consent:
            raise ReaderBlockedError(self.name, REASON_NO_CONSENT)
        super().ensure_may_read(item, on_date)

    def grant_consent(self) -> None:
        """Фиксирует согласие опекуна."""
        self.guardian_consent = True

    def revoke_consent(self) -> None:
        """Отзывает согласие опекуна."""
        self.guardian_consent = False

    def is_still_child(self, on_date: date) -> bool:
        """Проверяет, что читатель ещё не достиг совершеннолетия."""
        return not self.is_adult_on(on_date)

    def change_guardian(self, guardian: Reader, on_date: date) -> None:
        """Назначает нового опекуна, который должен быть совершеннолетним."""
        if not guardian.is_adult_on(on_date):
            raise ValidationError(FIELD_AGE, RULE_ADULT)
        self.guardian = guardian
