from .library_error import LibraryError


class RenewalNotAllowedError(LibraryError):
    """Продление выдачи невозможно."""

    MESSAGE_TEMPLATE = "Продление невозможно: {reason}."

    def __init__(self, reason: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(reason=reason))
