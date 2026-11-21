from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import CARD_VALIDITY_DAYS, FIELD_ID
from ..exceptions import CardExpiredError, ReaderBlockedError
from ..validation import require_text

if TYPE_CHECKING:
    from .reader import Reader


class LibraryCard:
    """Читательский билет."""

    def __init__(self, card_number: str, reader: Reader, issued_on: date):
        self.card_number = require_text(card_number, FIELD_ID)
        self.reader = reader
        self.issued_on = issued_on
        self.expires_on = issued_on + timedelta(days=CARD_VALIDITY_DAYS)
        self.is_blocked = False
        self.block_reason = ""

    def is_valid_on(self, on_date: date) -> bool:
        """Проверяет, что билет не заблокирован и не просрочен."""
        return not self.is_blocked and on_date <= self.expires_on

    def block(self, reason: str) -> None:
        """Блокирует билет с указанием причины."""
        self.is_blocked = True
        self.block_reason = reason.strip()

    def unblock(self) -> None:
        """Снимает блокировку билета."""
        self.is_blocked = False
        self.block_reason = ""

    def renew(self, on_date: date) -> None:
        """Продлевает билет на стандартный срок от большей из дат."""
        start = max(self.expires_on, on_date)
        self.expires_on = start + timedelta(days=CARD_VALIDITY_DAYS)

    def days_left(self, on_date: date) -> int:
        """Возвращает число оставшихся дней действия билета."""
        return max(0, (self.expires_on - on_date).days)

    def ensure_usable(self, on_date: date) -> None:
        """Бросает исключение, если билет нельзя использовать."""
        if self.is_blocked:
            raise ReaderBlockedError(self.reader.name, self.block_reason)
        if on_date > self.expires_on:
            raise CardExpiredError(self.card_number, self.expires_on.isoformat())
