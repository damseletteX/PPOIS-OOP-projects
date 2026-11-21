from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ..constants import FIELD_ID, FIELD_TEXT
from ..enums import NotificationChannel
from ..validation import require_text

if TYPE_CHECKING:
    from ..people.reader import Reader


class Notification:
    """Уведомление читателю."""

    def __init__(self, notification_id: str, reader: Reader, message: str, sent_on: date):
        self.notification_id = require_text(notification_id, FIELD_ID)
        self.reader = reader
        self.message = require_text(message, FIELD_TEXT)
        self.sent_on = sent_on
        self.channel = NotificationChannel.EMAIL if reader.email else NotificationChannel.SMS
        self.is_read = False

    def mark_read(self) -> None:
        """Отмечает уведомление прочитанным."""
        self.is_read = True

    def is_email(self) -> bool:
        """Проверяет, что уведомление отправлено по почте."""
        return self.channel == NotificationChannel.EMAIL

    def age_days(self, on_date: date) -> int:
        """Возвращает возраст уведомления в днях."""
        return (on_date - self.sent_on).days

    def address(self) -> str:
        """Возвращает адрес доставки: почту или телефон."""
        return self.reader.email if self.is_email() else self.reader.phone
