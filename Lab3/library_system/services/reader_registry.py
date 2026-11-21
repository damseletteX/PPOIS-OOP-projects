from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID, HISTORY_ENTRY_TEMPLATE, RULE_UNIQUE
from ..exceptions import ActiveLoansError, ReaderNotFoundError, ValidationError

if TYPE_CHECKING:
    from ..people.reader import Reader


class ReaderRegistry:
    """Реестр читателей библиотеки."""

    def __init__(self):
        self.readers: dict[str, Reader] = {}
        self.history: list[str] = []
        self.last_updated: date | None = None

    def register(self, reader: Reader, on_date: date) -> None:
        """Регистрирует читателя; идентификатор должен быть уникальным."""
        if reader.reader_id in self.readers:
            raise ValidationError(FIELD_ID, RULE_UNIQUE)
        self.readers[reader.reader_id] = reader
        self._log("регистрация", reader, on_date)

    def get(self, reader_id: str) -> Reader:
        """Возвращает читателя по идентификатору."""
        if reader_id not in self.readers:
            raise ReaderNotFoundError(reader_id)
        return self.readers[reader_id]

    def unregister(self, reader_id: str, on_date: date) -> Reader:
        """Снимает читателя с учёта, если у него нет невозвращённых изданий."""
        reader = self.get(reader_id)
        active_count = len(reader.active_loans())
        if active_count:
            raise ActiveLoansError(reader.name, active_count)
        del self.readers[reader_id]
        self._log("снятие с учёта", reader, on_date)
        return reader

    def find_by_name(self, fragment: str) -> list[Reader]:
        """Ищет читателей по части имени."""
        needle = fragment.strip().lower()
        return [reader for reader in self.readers.values() if needle in reader.name.lower()]

    def debtors(self) -> list[Reader]:
        """Возвращает читателей с неоплаченными штрафами."""
        return [reader for reader in self.readers.values() if reader.unpaid_fines_total() > 0]

    def with_overdue(self, on_date: date) -> list[Reader]:
        """Возвращает читателей с просроченными изданиями."""
        return [reader for reader in self.readers.values() if reader.overdue_loans(on_date)]

    def count_active(self) -> int:
        """Возвращает число активных читателей."""
        return sum(1 for reader in self.readers.values() if reader.is_active)

    def _log(self, action: str, reader: Reader, on_date: date) -> None:
        entry = HISTORY_ENTRY_TEMPLATE.format(
            date=on_date.isoformat(), action=action, name=reader.name
        )
        self.history.append(entry)
        self.last_updated = on_date
