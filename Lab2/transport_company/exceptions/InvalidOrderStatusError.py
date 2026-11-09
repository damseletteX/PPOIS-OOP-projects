from ..exceptions import TransportCompanyError

class InvalidOrderStatusError(TransportCompanyError, ValueError):
    """Недопустимый переход статуса заказа."""
