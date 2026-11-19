from .customer import Customer


class CorporateCustomer(Customer):
    """Организация, заказывающая перевозки."""

    def __init__(self, name: str, phone: str, address: str, tax_number: str, email: str = ""):
        super().__init__(name, phone, address, email)
        if not tax_number.strip():
            raise ValueError("Регистрационный номер обязателен.")

        self.tax_number = tax_number.strip()
        self.contact_person = ""
        self.contract_numbers = []
        self.credit_limit = 0.0

    def set_contact_person(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Укажите контактное лицо.")
        self.contact_person = name.strip()

    def add_contract(self, contract_number: str) -> None:
        if not contract_number.strip():
            raise ValueError("Номер договора не может быть пустым.")
        if contract_number in self.contract_numbers:
            raise ValueError("Такой договор уже зарегистрирован.")
        self.contract_numbers.append(contract_number)

    def set_credit_limit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Кредитный лимит не может быть отрицательным.")
        self.credit_limit = amount

    def can_pay_later(self, amount: float, debt: float = 0.0) -> bool:
        if amount < 0 or debt < 0:
            raise ValueError("Сумма и задолженность не могут быть отрицательными.")
        return debt + amount <= self.credit_limit