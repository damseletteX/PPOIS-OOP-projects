from __future__ import annotations

from typing import TYPE_CHECKING

from ..constants import FIELD_ID, RULE_UNIQUE
from ..exceptions import StaffNotFoundError, ValidationError
from ..people.director import Director
from ..people.librarian import Librarian

if TYPE_CHECKING:
    from ..facilities.branch import Branch
    from ..people.staff import Staff


class StaffRegistry:
    """Реестр сотрудников библиотеки."""

    def __init__(self):
        self.members: dict[str, Staff] = {}

    def hire(self, staff: Staff) -> None:
        """Принимает сотрудника; табельный номер должен быть уникальным."""
        if staff.staff_id in self.members:
            raise ValidationError(FIELD_ID, RULE_UNIQUE)
        self.members[staff.staff_id] = staff

    def get(self, staff_id: str) -> Staff:
        """Возвращает сотрудника по табельному номеру."""
        if staff_id not in self.members:
            raise StaffNotFoundError(staff_id)
        return self.members[staff_id]

    def get_librarian(self, staff_id: str) -> Librarian:
        """Возвращает сотрудника, если он библиотекарь."""
        staff = self.get(staff_id)
        if not isinstance(staff, Librarian):
            raise StaffNotFoundError(staff_id)
        return staff

    def get_director(self, staff_id: str) -> Director:
        """Возвращает сотрудника, если он директор."""
        staff = self.get(staff_id)
        if not isinstance(staff, Director):
            raise StaffNotFoundError(staff_id)
        return staff

    def dismiss(self, staff_id: str) -> Staff:
        """Увольняет сотрудника: деактивирует и убирает из филиала."""
        staff = self.get(staff_id)
        staff.deactivate()
        if staff.branch is not None:
            staff.branch.dismiss(staff)
        del self.members[staff_id]
        return staff

    def librarians(self) -> list[Librarian]:
        """Возвращает всех библиотекарей."""
        return [member for member in self.members.values() if isinstance(member, Librarian)]

    def by_branch(self, branch: Branch) -> list[Staff]:
        """Возвращает сотрудников филиала."""
        return [member for member in self.members.values() if member.branch is branch]

    def total_payroll(self) -> float:
        """Возвращает суммарный месячный оклад."""
        return sum(member.salary for member in self.members.values())
