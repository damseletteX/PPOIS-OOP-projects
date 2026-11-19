from .transport_company_error import TransportCompanyError

class InvalidOrderStatusError(TransportCompanyError, ValueError):
    """Недопустимый переход статуса заказа."""
