from datetime import date

from ..exceptions import (
    InvalidCargoError,
)
from .cargo import Cargo


class CargoDocument:
    """Сопроводительный документ на груз."""

    def __init__(
        self,
        document_id: str,
        cargo: Cargo,
        document_type: str,
        issue_date: date,
        issuer: str,
        expiry_date: date | None = None,
    ):
        if not document_id or not document_type or not issuer:
            raise InvalidCargoError("ID, тип документа и организация-выдаватель обязательны.")
        if expiry_date is not None and expiry_date < issue_date:
            raise InvalidCargoError("Документ не может истекать до выдачи.")

        self.document_id = document_id
        self.cargo = cargo
        self.document_type = document_type
        self.issue_date = issue_date
        self.issuer = issuer
        self.expiry_date = expiry_date
        self.document_number = ""
        self.is_verified = False
        self.notes = ""

    def verify(self):
        """Отмечает документ как проверенный."""
        self.is_verified = True

    def revoke_verification(self):
        """Отменяет отметку о проверке."""
        self.is_verified = False

    def is_expired(self, today: date | None = None) -> bool:
        """Проверяет, истёк ли срок действия документа."""
        today = today or date.today()
        return self.expiry_date is not None and today > self.expiry_date

    def update_number(self, document_number: str):
        """Устанавливает номер документа."""
        if not document_number:
            raise InvalidCargoError("Номер документа не может быть пустым.")
        self.document_number = document_number

    def add_note(self, note: str):
        """Добавляет примечание к документу."""
        if not note:
            raise InvalidCargoError("Примечание не может быть пустым.")
        self.notes = f"{self.notes}\n{note}".strip()
