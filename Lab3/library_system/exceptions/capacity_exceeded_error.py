from .library_error import LibraryError


class CapacityExceededError(LibraryError):
    """Превышена вместимость полки, зала или мероприятия."""

    MESSAGE_TEMPLATE = "«{place_name}»: свободных мест нет (вместимость {capacity})."

    def __init__(self, place_name: str, capacity: int):
        super().__init__(self.MESSAGE_TEMPLATE.format(place_name=place_name, capacity=capacity))
