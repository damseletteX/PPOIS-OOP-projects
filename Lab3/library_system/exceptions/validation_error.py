from .library_error import LibraryError


class ValidationError(LibraryError):
    """Некорректное значение поля."""

    MESSAGE_TEMPLATE = "Поле «{field_name}» {rule}."

    def __init__(self, field_name: str, rule: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(field_name=field_name, rule=rule))
