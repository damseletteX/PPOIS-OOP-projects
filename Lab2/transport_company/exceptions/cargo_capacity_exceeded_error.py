from .transport_company_error import TransportCompanyError


class CargoCapacityExceededError(TransportCompanyError):
    """Превышена грузоподъёмность транспортного средства."""
