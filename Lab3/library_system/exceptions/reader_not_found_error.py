from .library_error import LibraryError


class ReaderNotFoundError(LibraryError):
    """Читатель не найден в реестре."""

    MESSAGE_TEMPLATE = "Читатель «{reader_id}» не найден."

    def __init__(self, reader_id: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(reader_id=reader_id))
