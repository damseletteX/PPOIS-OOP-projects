class Person:
    """Базовый класс человека."""

    def __init__(self, name: str, phone: str, email: str = ""):
        if not name.strip():
            raise ValueError("Имя не может быть пустым.")
        if not phone.strip():
            raise ValueError("Телефон не может быть пустым.")

        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.is_active = True

    def update_phone(self, phone: str) -> None:
        if not phone.strip():
            raise ValueError("Телефон не может быть пустым.")
        self.phone = phone.strip()

    def update_email(self, email: str) -> None:
        self.email = email.strip()

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def contact_information(self) -> str:
        return f"{self.name}, телефон: {self.phone}, email: {self.email}"