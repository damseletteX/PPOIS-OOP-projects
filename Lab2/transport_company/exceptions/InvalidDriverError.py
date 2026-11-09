from ..exceptions import TransportCompanyError  # noqa: N999


class InvalidDriverError(TransportCompanyError, ValueError):
    """Некорректные данные водителя."""
