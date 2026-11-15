from .TransportCompanyError import TransportCompanyError


class InvalidVehicleError(TransportCompanyError, ValueError):
    """Некорректные данные транспортного средства."""
