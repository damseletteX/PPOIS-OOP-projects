from .Customer import Customer


class IndividualCustomer(Customer):
    """Частный клиент."""

    def __init__(
        self, name: str, phone: str, address: str, email: str = "", passport_number: str = ""
    ):
        super().__init__(name, phone, address, email)
        self.passport_number = passport_number.strip()
        self.preferred_contact = "phone"
        self.completed_orders = 0

    def set_preferred_contact(self, method: str) -> None:
        if method not in ("phone", "email"):
            raise ValueError("Способ связи: phone или email.")
        if method == "email" and not self.email:
            raise ValueError("Для связи по email укажите адрес.")
        self.preferred_contact = method

    def record_completed_order(self) -> None:
        self.completed_orders += 1

    def is_regular_customer(self) -> bool:
        return self.completed_orders >= 5

    def update_passport(self, passport_number: str) -> None:
        if not passport_number.strip():
            raise ValueError("Номер документа не может быть пустым.")
        self.passport_number = passport_number.strip()