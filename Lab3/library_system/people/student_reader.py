from __future__ import annotations

from datetime import date

from ..constants import (
    FIELD_COURSE,
    FIELD_NAME,
    MAX_COURSE,
    MIN_COURSE,
    STUDENT_BONUS_DAYS,
    STUDENT_EXTRA_LOANS,
)
from ..validation import require_in_range, require_text
from .reader import Reader


class StudentReader(Reader):
    """Читатель-студент с расширенными лимитами."""

    def __init__(
        self,
        reader_id: str,
        name: str,
        phone: str,
        birth_date: date,
        registered_on: date,
        student_number: str,
        university: str,
        course: int = MIN_COURSE,
        email: str = "",
    ):
        super().__init__(reader_id, name, phone, birth_date, registered_on, email)
        self.student_number = require_text(student_number, FIELD_NAME)
        self.university = require_text(university, FIELD_NAME)
        self.course = require_in_range(course, MIN_COURSE, MAX_COURSE, FIELD_COURSE)

    def loan_limit(self) -> int:
        """Студенту разрешено больше выдач одновременно."""
        return super().loan_limit() + STUDENT_EXTRA_LOANS

    def loan_bonus_days(self) -> int:
        """Студенту срок выдачи увеличен."""
        return STUDENT_BONUS_DAYS

    def advance_course(self) -> None:
        """Переводит студента на следующий курс."""
        self.course = require_in_range(self.course + 1, MIN_COURSE, MAX_COURSE, FIELD_COURSE)

    def is_final_year(self) -> bool:
        """Проверяет, что студент на последнем курсе."""
        return self.course == MAX_COURSE

    def change_university(self, university: str) -> None:
        """Меняет учебное заведение."""
        self.university = require_text(university, FIELD_NAME)
