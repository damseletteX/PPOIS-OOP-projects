"""Специализированные исключения транспортной компании."""


class TransportCompanyError(Exception):
    """Базовое исключение транспортной компании."""


class InvalidCustomerError(TransportCompanyError, ValueError):
    """Некорректные данные клиента."""


class InvalidDriverError(TransportCompanyError, ValueError):
    """Некорректные данные водителя."""


class InvalidVehicleError(TransportCompanyError, ValueError):
    """Некорректные данные транспортного средства."""


class VehicleUnavailableError(TransportCompanyError):
    """Транспортное средство недоступно."""


class DriverUnavailableError(TransportCompanyError):
    """Водитель недоступен."""


class InvalidCargoError(TransportCompanyError, ValueError):
    """Некорректные параметры груза."""


class CargoCapacityExceededError(TransportCompanyError):
    """Превышена грузоподъёмность транспортного средства."""


class InvalidRouteError(TransportCompanyError, ValueError):
    """Некорректный маршрут перевозки."""


class InvalidOrderStatusError(TransportCompanyError, ValueError):
    """Недопустимый переход статуса заказа."""


class PaymentError(TransportCompanyError):
    """Ошибка обработки оплаты."""


class DeliveryError(TransportCompanyError):
    """Ошибка выполнения доставки."""
