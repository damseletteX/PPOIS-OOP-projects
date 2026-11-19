from .transport_company_error import TransportCompanyError


class InvalidRouteError(TransportCompanyError, ValueError):
    """Некорректный маршрут перевозки."""
