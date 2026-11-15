from .TransportCompanyError import TransportCompanyError


class InvalidRouteError(TransportCompanyError, ValueError):
    """Некорректный маршрут перевозки."""
