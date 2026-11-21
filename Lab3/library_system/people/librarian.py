from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import DEFAULT_DESK_NUMBER, FIELD_LIMIT, FIELD_NAME
from ..validation import require_positive, require_text
from .staff import Staff

if TYPE_CHECKING:
    from ..circulation.loan import Loan


class Librarian(Staff):
    """Библиотекарь, работающий на кафедре выдачи."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        phone: str,
        birth_date: date,
        salary: float,
        hired_on: date,
        desk_number: int = DEFAULT_DESK_NUMBER,
        email: str = "",
    ):
        super().__init__(staff_id, name, phone, birth_date, salary, hired_on, email)
        self.desk_number = require_positive(desk_number, FIELD_LIMIT)
        self.issued_loans: list[Loan] = []
        self.languages: list[str] = []

    def register_issued_loan(self, loan: Loan) -> None:
        """Записывает выдачу, оформленную библиотекарем."""
        self.issued_loans.append(loan)

    def issued_count(self) -> int:
        """Возвращает общее число оформленных выдач."""
        return len(self.issued_loans)

    def issued_on(self, on_date: date) -> list[Loan]:
        """Возвращает выдачи, оформленные в указанный день."""
        return [loan for loan in self.issued_loans if loan.issued_on == on_date]

    def assign_desk(self, desk_number: int) -> None:
        """Переводит библиотекаря на другую кафедру."""
        self.desk_number = require_positive(desk_number, FIELD_LIMIT)

    def add_language(self, language: str) -> None:
        """Добавляет язык, на котором библиотекарь может консультировать."""
        cleaned = require_text(language, FIELD_NAME).lower()
        if cleaned not in self.languages:
            self.languages.append(cleaned)

    def speaks(self, language: str) -> bool:
        """Проверяет, консультирует ли библиотекарь на языке."""
        return language.strip().lower() in self.languages
