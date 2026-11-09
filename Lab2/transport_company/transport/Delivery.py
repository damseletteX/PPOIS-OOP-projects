from datetime import date, datetime
from .TransportOrder import TransportOrder
from ..exceptions import (
    DeliveryError,
)


class Delivery:
    """Доставка заказа получателю."""

    def __init__(
        self,
        delivery_id: str,
        order: TransportOrder,
        recipient: str,
        address: str,
        scheduled_date: date,
    ):
        if not delivery_id or not recipient or not address:
            raise DeliveryError("ID, получатель и адрес доставки обязательны.")

        self.delivery_id = delivery_id
        self.order = order
        self.recipient = recipient
        self.address = address
        self.scheduled_date = scheduled_date
        self.status = "scheduled"
        self.actual_delivery_time = None
        self.received_by = ""
        self.proof_of_delivery = ""
        self.failure_reason = ""

    def mark_in_transit(self):
        """Отмечает, что доставка находится в пути."""
        if self.status != "scheduled":
            raise DeliveryError("Доставку нельзя перевести в этот статус.")
        self.status = "in_transit"

    def confirm_delivery(self, received_by: str, proof: str = ""):
        """Подтверждает вручение заказа."""
        if self.status != "in_transit":
            raise DeliveryError("Подтвердить можно только доставку в пути.")
        if not received_by:
            raise DeliveryError("Укажите, кто принял груз.")

        self.received_by = received_by
        self.proof_of_delivery = proof
        self.actual_delivery_time = datetime.now()
        self.status = "delivered"

        if self.order.status == "in_transit":
            self.order.set_status("delivered")

    def report_failure(self, reason: str):
        """Фиксирует неудачную попытку доставки."""
        if self.status == "delivered":
            raise DeliveryError("Уже доставленную посылку нельзя отметить неудачной.")
        if not reason:
            raise DeliveryError("Укажите причину неудачной доставки.")
        self.failure_reason = reason
        self.status = "failed"

    def reschedule(self, new_date: date):
        """Переносит дату доставки."""
        if self.status == "delivered":
            raise DeliveryError("Нельзя перенести уже завершённую доставку.")
        if new_date < date.today():
            raise DeliveryError("Новая дата не может быть в прошлом.")
        self.scheduled_date = new_date
        self.status = "scheduled"

    def is_late(self, today: date | None = None) -> bool:
        """Проверяет просрочку ещё не завершённой доставки."""
        today = today or date.today()
        return self.status != "delivered" and today > self.scheduled_date

    def record_recipient(self, recipient: str):
        """Обновляет имя получателя."""
        if not recipient:
            raise DeliveryError("Имя получателя не может быть пустым.")
        self.recipient = recipient