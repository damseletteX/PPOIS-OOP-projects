from ..exceptions import TransportCompanyError


class InvalidCustomerError(TransportCompanyError, ValueError):
    """Некорректные данные клиента."""
