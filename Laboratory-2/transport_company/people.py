"""Domain classes for the transport company. Standard library only."""
from typing import Optional

class Person:
    """Domain entity: Person. Доменная сущность транспортной компании."""
    def __init__(self, name: str, email: str, phone: str, address: str, related_entity_id: Optional[str] = None, notes: str = ''):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.related_entity_id = related_entity_id
        self.notes = notes

    def update_contact_details(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет новые контактные данные и обновляет только переданные непустые значения; сохраняет прежние значения остальных полей.'

    def verify_identity(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет наличие имени и контактных/идентификационных данных; при недостатке данных отклоняет операцию.'

class Customer:
    """Domain entity: Customer. Доменная сущность транспортной компании."""
    def __init__(self, customer_code: str, billing_address: str, preferred_contact: str, credit_limit: float, related_entity_id: Optional[str] = None, notes: str = ''):
        self.customer_code = customer_code
        self.billing_address = billing_address
        self.preferred_contact = preferred_contact
        self.credit_limit = credit_limit
        self.related_entity_id = related_entity_id
        self.notes = notes

    def place_order(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет кредитный лимит и обязательные данные заказа; формирует заказ со статусом «создан».'

    def request_delivery_quote(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Принимает параметры груза и маршрута, проверяет их и возвращает расчётную стоимость.'

class BusinessCustomer:
    """Domain entity: BusinessCustomer. Доменная сущность транспортной компании."""
    def __init__(self, company_name: str, tax_number: str, contract_number: str, payment_terms_days: int, related_entity_id: Optional[str] = None, notes: str = ''):
        self.company_name = company_name
        self.tax_number = tax_number
        self.contract_number = contract_number
        self.payment_terms_days = payment_terms_days
        self.related_entity_id = related_entity_id
        self.notes = notes

    def approve_contract_terms(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет срок оплаты и наличие номера договора; переводит договор в состояние «одобрен».'

    def request_monthly_statement(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Формирует перечень счетов и платежей клиента за запрошенный месяц.'

class PrivateCustomer:
    """Domain entity: PrivateCustomer. Доменная сущность транспортной компании."""
    def __init__(self, identity_document: str, delivery_instructions: str, notification_opt_in: bool, customer_since: str, related_entity_id: Optional[str] = None, notes: str = ''):
        self.identity_document = identity_document
        self.delivery_instructions = delivery_instructions
        self.notification_opt_in = notification_opt_in
        self.customer_since = customer_since
        self.related_entity_id = related_entity_id
        self.notes = notes

    def confirm_delivery_address(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет адрес доставки и фиксирует подтверждение адреса.'

    def change_notification_preferences(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Изменяет согласие на уведомления и возвращает актуальное значение настройки.'

class Employee:
    """Domain entity: Employee. Доменная сущность транспортной компании."""
    def __init__(self, employee_number: str, hire_date: str, salary: float, employment_status: str, related_entity_id: Optional[str] = None, notes: str = ''):
        self.employee_number = employee_number
        self.hire_date = hire_date
        self.salary = salary
        self.employment_status = employment_status
        self.related_entity_id = related_entity_id
        self.notes = notes

    def request_leave(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет статус сотрудника и отсутствие пересекающегося отпуска; регистрирует заявку.'

    def record_performance_review(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сохраняет оценку, дату и комментарий к результатам работы сотрудника.'

class Driver:
    """Domain entity: Driver. Доменная сущность транспортной компании."""
    def __init__(self, license_number: str, license_category: str, license_expiry: str, hours_driven_today: float, related_entity_id: Optional[str] = None, notes: str = ''):
        self.license_number = license_number
        self.license_category = license_category
        self.license_expiry = license_expiry
        self.hours_driven_today = hours_driven_today
        self.related_entity_id = related_entity_id
        self.notes = notes

    def accept_assignment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет действительность водительского удостоверения, категорию и допустимое время управления; принимает назначение.'

    def record_driver_inspection(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Фиксирует предрейсовую проверку водителя и выявленные замечания.'

    def report_fatigue(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Регистрирует усталость водителя и помечает его недоступным до подтверждения готовности.'

class Dispatcher:
    """Domain entity: Dispatcher. Доменная сущность транспортной компании."""
    def __init__(self, dispatch_area: str, shift_start: str, shift_end: str, active_assignments: int, related_entity_id: Optional[str] = None, notes: str = ''):
        self.dispatch_area = dispatch_area
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.active_assignments = active_assignments
        self.related_entity_id = related_entity_id
        self.notes = notes

    def assign_vehicle_to_trip(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет доступность и пригодность машины для рейса; закрепляет транспорт за рейсом.'

    def reassign_trip(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Снимает прежнее назначение и назначает доступный альтернативный ресурс, сохраняя историю изменения.'

    def resolve_dispatch_conflict(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Выявляет двойное назначение водителя/машины и оставляет только непротиворечивое назначение.'

class Mechanic:
    """Domain entity: Mechanic. Доменная сущность транспортной компании."""
    def __init__(self, specialization: str, certification_code: str, workshop_id: str, open_work_orders: int, related_entity_id: Optional[str] = None, notes: str = ''):
        self.specialization = specialization
        self.certification_code = certification_code
        self.workshop_id = workshop_id
        self.open_work_orders = open_work_orders
        self.related_entity_id = related_entity_id
        self.notes = notes

    def diagnose_vehicle_fault(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сопоставляет симптомы с профилем механика и формирует перечень вероятных неисправностей.'

    def complete_repair_job(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет выполненные работы и стоимость, закрывает заказ-наряд и обновляет доступность транспорта.'

class Manager:
    """Domain entity: Manager. Доменная сущность транспортной компании."""
    def __init__(self, department: str, approval_limit: float, management_level: int, reports_to: str, related_entity_id: Optional[str] = None, notes: str = ''):
        self.department = department
        self.approval_limit = approval_limit
        self.management_level = management_level
        self.reports_to = reports_to
        self.related_entity_id = related_entity_id
        self.notes = notes

    def approve_expense(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сравнивает сумму расхода с лимитом полномочий менеджера; утверждает расход или отклоняет его.'

    def review_operational_metrics(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Рассчитывает и возвращает сводные показатели выполнения рейсов, затрат и своевременности.'

class WarehouseWorker:
    """Domain entity: WarehouseWorker. Доменная сущность транспортной компании."""
    def __init__(self, warehouse_id: str, safety_training_date: str, forklift_certified: bool, assigned_zone: str, related_entity_id: Optional[str] = None, notes: str = ''):
        self.warehouse_id = warehouse_id
        self.safety_training_date = safety_training_date
        self.forklift_certified = forklift_certified
        self.assigned_zone = assigned_zone
        self.related_entity_id = related_entity_id
        self.notes = notes

    def record_loading_activity(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Регистрирует время, груз, зону и сотрудника, выполнившего погрузку.'

    def confirm_cargo_staging(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет размещение груза в назначенной зоне и отмечает готовность к погрузке.'

