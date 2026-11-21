from .library_error import LibraryError


class PaymentError(LibraryError):
    """Ошибка оплаты штрафа или взноса."""

    MESSAGE_TEMPLATE = "Оплата невозможна: {reason}."

    def __init__(self, reason: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(reason=reason))
