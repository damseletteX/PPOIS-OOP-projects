from ..exceptions import TransportCompanyError


class InvalidRouteError(TransportCompanyError, ValueError):
    """Некорректный маршрут перевозки."""
