from .library_error import LibraryError


class ActiveLoansError(LibraryError):
    """Операция невозможна, пока у читателя есть невозвращённые издания."""

    MESSAGE_TEMPLATE = "У читателя «{reader_name}» не возвращено изданий: {count}."

    def __init__(self, reader_name: str, count: int):
        super().__init__(self.MESSAGE_TEMPLATE.format(reader_name=reader_name, count=count))
