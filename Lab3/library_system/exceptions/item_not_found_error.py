from .library_error import LibraryError


class ItemNotFoundError(LibraryError):
    """Издание или экземпляр не найдены в каталоге."""

    MESSAGE_TEMPLATE = "Издание или экземпляр «{item_id}» не найдены."

    def __init__(self, item_id: str):
        super().__init__(self.MESSAGE_TEMPLATE.format(item_id=item_id))
