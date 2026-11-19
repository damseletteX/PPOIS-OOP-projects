from .transport_company_error import TransportCompanyError


class InvalidVehicleError(TransportCompanyError, ValueError):
    """Некорректные данные транспортного средства."""
