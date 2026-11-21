from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..constants import FIELD_ADDRESS, FIELD_ID, FIELD_NAME, FIELD_PHONE, RULE_NOT_IN_STAFF
from ..exceptions import CapacityExceededError, ItemNotFoundError, ValidationError
from ..validation import require_text

if TYPE_CHECKING:
    from ..catalog.item_copy import ItemCopy
    from ..people.staff import Staff
    from .opening_hours import OpeningHours
    from .reading_room import ReadingRoom
    from .shelf import Shelf


class Branch:
    """Филиал библиотеки."""

    def __init__(
        self,
        branch_id: str,
        name: str,
        address: str,
        phone: str,
        opening_hours: OpeningHours,
    ):
        self.branch_id = require_text(branch_id, FIELD_ID)
        self.name = require_text(name, FIELD_NAME)
        self.address = require_text(address, FIELD_ADDRESS)
        self.phone = require_text(phone, FIELD_PHONE)
        self.opening_hours = opening_hours
        self.rooms: list[ReadingRoom] = []
        self.shelves: list[Shelf] = []
        self.staff: list[Staff] = []
        self.manager: Staff | None = None

    def add_room(self, room: ReadingRoom) -> None:
        """Добавляет читальный зал."""
        self.rooms.append(room)

    def get_room(self, room_id: str) -> ReadingRoom:
        """Возвращает читальный зал по идентификатору."""
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        raise ItemNotFoundError(room_id)

    def add_shelf(self, shelf: Shelf) -> None:
        """Добавляет полку."""
        self.shelves.append(shelf)

    def hire(self, staff: Staff) -> None:
        """Принимает сотрудника в филиал."""
        if staff not in self.staff:
            self.staff.append(staff)
            staff.assign_branch(self)

    def dismiss(self, staff: Staff) -> None:
        """Выводит сотрудника из состава филиала."""
        if staff in self.staff:
            self.staff.remove(staff)
        if self.manager is staff:
            self.manager = None

    def set_manager(self, staff: Staff) -> None:
        """Назначает заведующего из числа сотрудников филиала."""
        if staff not in self.staff:
            raise ValidationError(FIELD_NAME, RULE_NOT_IN_STAFF)
        self.manager = staff

    def find_free_shelf(self) -> Shelf:
        """Возвращает первую полку со свободным местом."""
        for shelf in self.shelves:
            if not shelf.is_full():
                return shelf
        raise CapacityExceededError(self.name, self.total_capacity())

    def total_capacity(self) -> int:
        """Возвращает суммарную вместимость полок."""
        return sum(shelf.capacity for shelf in self.shelves)

    def all_copies(self) -> list[ItemCopy]:
        """Возвращает все экземпляры, стоящие на полках филиала."""
        return [copy for shelf in self.shelves for copy in shelf.copies]

    def staff_count(self) -> int:
        """Возвращает число сотрудников."""
        return len(self.staff)

    def payroll(self) -> float:
        """Возвращает месячный фонд оплаты труда."""
        return sum(member.salary for member in self.staff)

    def is_open_at(self, moment: datetime) -> bool:
        """Проверяет, открыт ли филиал в указанный момент."""
        return self.opening_hours.is_open_at(moment)
