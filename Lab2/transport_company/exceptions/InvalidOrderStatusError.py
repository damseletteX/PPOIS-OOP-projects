from .TransportCompanyError import TransportCompanyError

class InvalidOrderStatusError(TransportCompanyError, ValueError):
    """Недопустимый переход статуса заказа."""
