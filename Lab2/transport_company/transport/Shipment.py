from datetime import date, datetime
from .TransportOrder import TransportOrder
from ..vehicles.Vehicle import Vehicle
from ..exceptions import (
    InvalidOrderStatusError,
    InvalidCargoError,
    CargoCapacityExceededError,
    VehicleUnavailableError,
    DeliveryError,
)


class Shipment:
    """Подготовленная партия груза."""

    def __init__(
        self,
        shipment_id: str,
        order: TransportOrder,
        prepared_date: date | None = None,
    ):
        if not shipment_id:
            raise InvalidOrderStatusError("ID отправления обязателен.")

        self.shipment_id = shipment_id
        self.order = order
        self.prepared_date = prepared_date or date.today()
        self.items = list(order.items)
        self.is_ready = False
        self.loaded_vehicle = None
        self.loading_time = None
        self.unloading_time = None
        self.seal_number = ""

    def check_readiness(self) -> bool:
        """Проверяет готовность отправления к перевозке."""
        return bool(self.items) and all(item.cargo.is_packed for item in self.items)

    def prepare(self):
        """Подтверждает готовность отправления."""
        if not self.check_readiness():
            raise DeliveryError("Не все грузы упакованы или отправление пустое.")
        self.is_ready = True

    def load_onto(self, vehicle: Vehicle):
        """Загружает отправление на подходящий транспорт."""
        if not self.is_ready:
            raise DeliveryError("Сначала подготовьте отправление.")
        if not vehicle.is_available:
            raise VehicleUnavailableError("Транспорт недоступен.")

        if hasattr(vehicle, "tank_volume_liters"):
            raise InvalidCargoError(
                "Для цистерны требуется отдельная проверка совместимости груза."
            )

        total_weight = sum(item.total_weight() for item in self.items)
        total_volume = sum(item.total_volume() for item in self.items)

        if total_weight > vehicle.capacity_kg:
            raise CargoCapacityExceededError("Превышена грузоподъёмность.")

        vehicle_volume = getattr(vehicle, "cargo_volume_m3", None)
        if vehicle_volume is not None and total_volume > vehicle_volume:
            raise CargoCapacityExceededError("Превышен объём кузова.")

        self.loaded_vehicle = vehicle
        self.loading_time = datetime.now()

        for item in self.items:
            item.mark_loaded()

        vehicle.mark_unavailable()

    def unload(self):
        """Фиксирует выгрузку отправления."""
        if self.loaded_vehicle is None:
            raise DeliveryError("Отправление ещё не загружено.")

        for item in self.items:
            item.mark_unloaded()

        self.unloading_time = datetime.now()
        self.loaded_vehicle.mark_available()
        self.loaded_vehicle = None

    def set_seal_number(self, seal_number: str):
        """Устанавливает номер пломбы отправления."""
        if not seal_number:
            raise DeliveryError("Номер пломбы не может быть пустым.")
        self.seal_number = seal_number