from .library_error import LibraryError


class ItemNotAvailableError(LibraryError):
    """Нет свободных экземпляров издания."""

    MESSAGE_TEMPLATE = "Издание «{title}» сейчас недоступно для выдачи."

    def __init__(self, title: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(title=title))
