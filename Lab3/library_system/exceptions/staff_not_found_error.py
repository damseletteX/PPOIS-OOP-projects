from .library_error import LibraryError


class StaffNotFoundError(LibraryError):
    """Сотрудник не найден в реестре."""

    MESSAGE_TEMPLATE = "Сотрудник «{staff_id}» не найден."

    def __init__(self, staff_id: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(staff_id=staff_id))
