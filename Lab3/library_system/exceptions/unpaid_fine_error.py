from .library_error import LibraryError


class UnpaidFineError(LibraryError):
    """У читателя непогашенные штрафы выше допустимого порога."""

    MESSAGE_TEMPLATE = "У читателя «{reader_name}» непогашенные штрафы: {amount:.2f}."

    def __init__(self, reader_name: str, amount: float):
        super().__init__(self.MESSAGE_TEMPLATE.format(reader_name=reader_name, amount=amount))
