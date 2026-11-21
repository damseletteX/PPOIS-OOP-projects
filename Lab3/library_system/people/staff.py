from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import (
    CURRENCY_DIGITS,
    DAYS_IN_YEAR,
    FIELD_ID,
    FIELD_PERCENT,
    FIELD_SALARY,
    FIELD_TIME,
    MAX_SALARY_RAISE_PERCENT,
    MONTHS_IN_YEAR,
    PERCENT_BASE,
    RULE_SHIFT_OVERLAP,
)
from ..exceptions import ValidationError
from ..validation import require_in_range, require_non_negative, require_text
from .person import Person

if TYPE_CHECKING:
    from ..facilities.branch import Branch
    from ..facilities.staff_shift import StaffShift


class Staff(Person):
    """Сотрудник библиотеки."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        phone: str,
        birth_date: date,
        salary: float,
        hired_on: date,
        email: str = "",
    ):
        super().__init__(name, phone, birth_date, email)
        self.staff_id = require_text(staff_id, FIELD_ID)
        self.salary = require_non_negative(salary, FIELD_SALARY)
        self.hired_on = hired_on
        self.branch: Branch | None = None
        self.shifts: list[StaffShift] = []

    def assign_branch(self, branch: Branch) -> None:
        """Прикрепляет сотрудника к филиалу."""
        self.branch = branch

    def raise_salary(self, percent: float) -> None:
        """Повышает оклад на процент в допустимых пределах."""
        require_in_range(percent, 0, MAX_SALARY_RAISE_PERCENT, FIELD_PERCENT)
        self.salary = round(self.salary * (PERCENT_BASE + percent) / PERCENT_BASE, CURRENCY_DIGITS)

    def annual_salary(self) -> float:
        """Возвращает годовой доход по окладу."""
        return self.salary * MONTHS_IN_YEAR

    def years_of_service(self, on_date: date) -> int:
        """Возвращает полное число лет стажа."""
        return max(0, (on_date - self.hired_on).days // DAYS_IN_YEAR)

    def add_shift(self, shift: StaffShift) -> None:
        """Добавляет смену, если она не пересекается с существующими."""
        if any(shift.overlaps(existing) for existing in self.shifts):
            raise ValidationError(FIELD_TIME, RULE_SHIFT_OVERLAP)
        self.shifts.append(shift)

    def works_on(self, on_date: date) -> bool:
        """Проверяет, есть ли у сотрудника смена в этот день."""
        return any(shift.shift_date == on_date for shift in self.shifts)

    def shift_hours_on(self, on_date: date) -> float:
        """Возвращает число рабочих часов за день."""
        return sum(item.duration_hours() for item in self.shifts if item.shift_date == on_date)
