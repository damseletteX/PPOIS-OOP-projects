from .library_error import LibraryError


class CardExpiredError(LibraryError):
    """Срок действия читательского билета истёк."""

    MESSAGE_TEMPLATE = "Срок действия билета «{card_number}» истёк {expired_on}."

    def __init__(self, card_number: str, expired_on: str):
        super().__init__(
            self.MESSAGE_TEMPLATE.format(card_number=card_number, expired_on=expired_on)
        )
