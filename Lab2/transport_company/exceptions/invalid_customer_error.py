from .transport_company_error import TransportCompanyError


class InvalidCustomerError(TransportCompanyError, ValueError):
    """Некорректные данные клиента."""
