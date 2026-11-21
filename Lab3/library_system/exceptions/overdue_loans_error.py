from .library_error import LibraryError


class OverdueLoansError(LibraryError):
    """У читателя есть просроченные выдачи."""

    MESSAGE_TEMPLATE = "У читателя «{reader_name}» просрочено изданий: {count}."

    def __init__(self, reader_name: str, count: int):
        super().__init__(self.MESSAGE_TEMPLATE.format(reader_name=reader_name, count=count))
