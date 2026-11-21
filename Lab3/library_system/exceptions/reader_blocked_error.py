from .library_error import LibraryError


class ReaderBlockedError(LibraryError):
    """Читательский билет заблокирован или читатель неактивен."""

    MESSAGE_TEMPLATE = "Читатель «{reader_name}» заблокирован: {reason}."

    def __init__(self, reader_name: str, reason: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(reader_name=reader_name, reason=reason))
