from .TransportCompanyError import TransportCompanyError  # noqa: N999


class CargoCapacityExceededError(TransportCompanyError):
    """Превышена грузоподъёмность транспортного средства."""
