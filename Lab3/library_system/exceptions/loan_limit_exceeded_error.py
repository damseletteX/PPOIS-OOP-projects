from .library_error import LibraryError


class LoanLimitExceededError(LibraryError):
    """Читатель достиг лимита одновременных выдач."""

    MESSAGE_TEMPLATE = "Читатель «{reader_name}» уже взял максимум изданий: {limit}."

    def __init__(self, reader_name: str, limit: int):
        super().__init__(self.MESSAGE_TEMPLATE.format(reader_name=reader_name, limit=limit))
