from .library_error import LibraryError


class BudgetExceededError(LibraryError):
    """Затраты превышают остаток бюджета."""

    MESSAGE_TEMPLATE = "Недостаточно бюджета: требуется {required:.2f}, доступно {available:.2f}."

    def __init__(self, required: float, available: float):
        super().__init__(self.MESSAGE_TEMPLATE.format(required=required, available=available))
