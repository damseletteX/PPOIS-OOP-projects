from .transport_company_error import TransportCompanyError


class InvalidDriverError(TransportCompanyError, ValueError):
    """Некорректные данные водителя."""
