
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


class Customer(Person):
    """Общий класс клиентов транспортной компании."""

    def __init__(self, name: str, phone: str, address: str,
                 email: str = ""):
        super().__init__(name, phone, email)
        if not address.strip():
            raise ValueError("Адрес не может быть пустым.")

        self.address = address.strip()
        self.orders = []
        self.discount_percent = 0
        self.is_verified = False

    def add_order(self, order) -> None:
        if not self.is_active:
            raise ValueError("Неактивный клиент не может оформлять заказы.")
        if order in self.orders:
            raise ValueError("Этот заказ уже добавлен клиенту.")
        self.orders.append(order)

    def remove_order(self, order) -> None:
        if order not in self.orders:
            raise ValueError("Заказ не найден у этого клиента.")
        self.orders.remove(order)

    def verify_customer(self) -> None:
        self.is_verified = True

    def set_discount(self, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Скидка должна быть от 0 до 100%.")
        self.discount_percent = percent

    def calculate_discount(self, amount: float) -> float:
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной.")
        return amount * self.discount_percent / 100

    def get_order_count(self) -> int:
        return len(self.orders)

    def change_address(self, address: str) -> None:
        if not address.strip():
            raise ValueError("Адрес не может быть пустым.")
        self.address = address.strip()


class IndividualCustomer(Customer):
    """Частный клиент."""

    def __init__(self, name: str, phone: str, address: str,
                 email: str = "", passport_number: str = ""):
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


class CorporateCustomer(Customer):
    """Организация, заказывающая перевозки."""

    def __init__(self, name: str, phone: str, address: str,
                 tax_number: str, email: str = ""):
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


class Employee(Person):
    """Базовый класс сотрудника."""

    def __init__(self, name: str, phone: str, employee_id: str,
                 salary: float, email: str = ""):
        super().__init__(name, phone, email)
        if not employee_id.strip():
            raise ValueError("Табельный номер обязателен.")
        if salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")

        self.employee_id = employee_id.strip()
        self.salary = salary
        self.department = "Transport"
        self.is_available = True
        self.assigned_tasks = []

    def assign_task(self, task: str) -> None:
        if not self.is_active:
            raise ValueError("Нельзя назначить задачу неактивному сотруднику.")
        if not task.strip():
            raise ValueError("Описание задачи не может быть пустым.")
        self.assigned_tasks.append(task.strip())
        self.is_available = False

    def complete_task(self, task: str) -> None:
        if task not in self.assigned_tasks:
            raise ValueError("Такая задача сотруднику не назначена.")
        self.assigned_tasks.remove(task)
        self.is_available = len(self.assigned_tasks) == 0

    def change_department(self, department: str) -> None:
        if not department.strip():
            raise ValueError("Название отдела не может быть пустым.")
        self.department = department.strip()

    def calculate_annual_salary(self) -> float:
        return self.salary * 12

    def is_ready_for_work(self) -> bool:
        return self.is_active and self.is_available


class Driver(Employee):
    """Водитель транспортной компании."""

    def __init__(self, name: str, phone: str, employee_id: str,
                 salary: float, license_number: str,
                 license_categories: list[str], experience_years: int,
                 email: str = ""):
        super().__init__(name, phone, employee_id, salary, email)
        if not license_number.strip():
            raise ValueError("Номер водительского удостоверения обязателен.")
        if experience_years < 0:
            raise ValueError("Стаж не может быть отрицательным.")
        if not license_categories:
            raise ValueError("Укажите хотя бы одну категорию прав.")

        self.license_number = license_number.strip()
        self.license_categories = set(license_categories)
        self.experience_years = experience_years
        self.assigned_vehicle = None
        self.completed_trips = 0
        self.is_on_trip = False

    def can_drive_category(self, category: str) -> bool:
        return category in self.license_categories

    def assign_vehicle(self, vehicle) -> None:
        if not self.is_ready_for_work():
            raise ValueError("Водитель сейчас недоступен.")
        if self.is_on_trip:
            raise ValueError("Водитель уже находится в рейсе.")
        if not getattr(vehicle, "is_available", False):
            raise ValueError("Транспортное средство недоступно.")

        required_category = getattr(vehicle, "required_license_category", None)
        if required_category and not self.can_drive_category(required_category):
            raise ValueError("У водителя нет нужной категории прав.")

        self.assigned_vehicle = vehicle

    def start_trip(self) -> None:
        if not self.is_ready_for_work():
            raise ValueError("Водитель не готов к работе.")
        if self.assigned_vehicle is None:
            raise ValueError("Сначала назначьте транспорт.")
        if self.is_on_trip:
            raise ValueError("Водитель уже находится в рейсе.")

        self.is_on_trip = True
        self.is_available = False
        self.assigned_vehicle.is_available = False

    def finish_trip(self) -> None:
        if not self.is_on_trip:
            raise ValueError("У водителя нет активного рейса.")

        self.is_on_trip = False
        self.is_available = True
        self.completed_trips += 1
        self.assigned_vehicle.is_available = True
        self.assigned_vehicle = None

    def is_experienced(self, minimum_years: int = 3) -> bool:
        return self.experience_years >= minimum_years

    def update_license_categories(self, categories: list[str]) -> None:
        if not categories:
            raise ValueError("Нужна хотя бы одна категория прав.")
        self.license_categories = set(categories)


class Dispatcher(Employee):
    """Диспетчер, координирующий перевозки."""

    def __init__(self, name: str, phone: str, employee_id: str,
                 salary: float, email: str = ""):
        super().__init__(name, phone, employee_id, salary, email)
        self.managed_trips = []
        self.shift = "day"
        self.max_trips = 20

    def register_trip(self, trip) -> None:
        if not self.is_active:
            raise ValueError("Неактивный диспетчер не может вести рейсы.")
        if trip in self.managed_trips:
            raise ValueError("Этот рейс уже зарегистрирован.")
        if len(self.managed_trips) >= self.max_trips:
            raise ValueError("Диспетчер достиг лимита рейсов.")
        self.managed_trips.append(trip)

    def close_trip(self, trip) -> None:
        if trip not in self.managed_trips:
            raise ValueError("Рейс не закреплён за диспетчером.")
        self.managed_trips.remove(trip)

    def set_shift(self, shift: str) -> None:
        if shift not in ("day", "night"):
            raise ValueError("Смена должна быть day или night.")
        self.shift = shift

    def find_managed_trip(self, trip_id: str):
        for trip in self.managed_trips:
            if getattr(trip, "trip_id", None) == trip_id:
                return trip
        return None

    def has_free_capacity(self) -> bool:
        return len(self.managed_trips) < self.max_trips


class Manager(Employee):
    """Менеджер, отвечающий за клиентов и заказы."""

    def __init__(self, name: str, phone: str, employee_id: str,
                 salary: float, email: str = ""):
        super().__init__(name, phone, employee_id, salary, email)
        self.managed_customers = []
        self.approved_orders = []
        self.monthly_target = 0.0
        self.monthly_revenue = 0.0

    def register_customer(self, customer: Customer) -> None:
        if customer in self.managed_customers:
            raise ValueError("Клиент уже закреплён за менеджером.")
        self.managed_customers.append(customer)

    def approve_order(self, order) -> None:
        if not self.is_active:
            raise ValueError("Неактивный менеджер не может одобрять заказы.")
        if order in self.approved_orders:
            raise ValueError("Заказ уже одобрен.")

        status = getattr(order, "status", None)
        if status not in ("new", "pending"):
            raise ValueError("Можно одобрить только новый или ожидающий заказ.")

        order.status = "approved"
        self.approved_orders.append(order)

    def set_monthly_target(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("План выручки не может быть отрицательным.")
        self.monthly_target = amount

    def record_revenue(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Выручка не может быть отрицательной.")
        self.monthly_revenue += amount

    def calculate_target_completion(self) -> float:
        if self.monthly_target == 0:
            return 0.0
        return self.monthly_revenue / self.monthly_target * 100

    def remove_customer(self, customer: Customer) -> None:
        if customer not in self.managed_customers:
            raise ValueError("Клиент не закреплён за этим менеджером.")
        self.managed_customers.remove(customer)
