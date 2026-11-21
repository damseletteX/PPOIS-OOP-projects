from .library_error import LibraryError


class InvalidStatusTransitionError(LibraryError):
    """Недопустимая смена статуса объекта."""

    MESSAGE_TEMPLATE = "{entity}: переход из «{current}» в «{target}» невозможен."

    def __init__(self, entity: str, current: str, target: str):
        super().__init__(
            self.MESSAGE_TEMPLATE.format(entity=entity, current=current, target=target)
        )
