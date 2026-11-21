from .library_error import LibraryError


class ReservationError(LibraryError):
    """Ошибка бронирования издания."""

    MESSAGE_TEMPLATE = "Бронирование невозможно: {reason}."

    def __init__(self, reason: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(reason=reason))
