from ..exceptions import TransportCompanyError


class InvalidCargoError(TransportCompanyError, ValueError):
    """Некорректные параметры груза."""
