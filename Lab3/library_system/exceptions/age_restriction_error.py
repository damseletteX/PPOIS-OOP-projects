from .library_error import LibraryError


class AgeRestrictionError(LibraryError):
    """Издание не подходит читателю по возрасту."""

    MESSAGE_TEMPLATE = "Издание «{title}» доступно с {min_age} лет."

    def __init__(self, title: str, min_age: int):
        super().__init__(self.MESSAGE_TEMPLATE.format(title=title, min_age=min_age))
