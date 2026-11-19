from .transport_company_error import TransportCompanyError


class InvalidCargoError(TransportCompanyError, ValueError):
    """Некорректные параметры груза."""
