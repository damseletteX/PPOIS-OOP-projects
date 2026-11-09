from datetime import date, datetime

from .Branch import Branch
from .CompanyPolicy import CompanyPolicy
from .CustomerRegistry import CustomerRegistry
from .Department import Department
from .EmployeeRegistry import EmployeeRegistry
from .Fleet import Fleet
from .OrderRegistry import OrderRegistry
from ..exceptions import (
    DeliveryError,
    InvalidCustomerError,
    InvalidDriverError,
    InvalidOrderStatusError,
    InvalidVehicleError,
)


class TransportCompany:
    """Главный объект, объединяющий подразделения компании."""

    def __init__(
        self,
        company_id: str,
        name: str,
        legal_name: str,
        tax_id: str,
        address: str,
        phone: str,
        email: str,
        founded_date: date | None = None,
    ):
        if not company_id or not name or not legal_name:
            raise ValueError("Не указаны основные данные компании.")
        if not tax_id:
            raise ValueError("Не указан налоговый идентификатор.")

        self.company_id = company_id
        self.name = name
        self.legal_name = legal_name
        self.tax_id = tax_id
        self.address = address
        self.phone = phone
        self.email = email
        self.founded_date = founded_date or date.today()

        self.branches = {}
        self.departments = {}
        self.fleet = Fleet(
            fleet_id=f"{company_id}-FLEET",
            name=f"Автопарк {name}",
        )
        self.employee_registry = EmployeeRegistry()
        self.customer_registry = CustomerRegistry()
        self.order_registry = OrderRegistry()

        self.policies = {}
        self.financial_reports = []
        self.is_active = True
        self.creation_time = datetime.now()
        self.notes = []

    def add_branch(self, branch: Branch):
        """Добавляет филиал компании."""
        if branch.branch_id in self.branches:
            raise ValueError("Филиал с таким идентификатором уже существует.")

        self.branches[branch.branch_id] = branch

    def remove_branch(self, branch_id: str):
        """Удаляет неактивный филиал без сотрудников и транспорта."""
        branch = self.branches.get(branch_id)

        if branch is None:
            return False
        if branch.employees or branch.vehicles or branch.warehouses:
            raise ValueError("Перед удалением филиала необходимо освободить его ресурсы.")

        del self.branches[branch_id]
        return True

    def get_branch(self, branch_id: str):
        """Находит филиал по идентификатору."""
        return self.branches.get(branch_id)

    def add_department(self, department: Department):
        """Добавляет подразделение компании."""
        if department.department_id in self.departments:
            raise ValueError("Подразделение с таким идентификатором уже существует.")

        self.departments[department.department_id] = department

    def remove_department(self, department_id: str):
        """Удаляет пустое подразделение."""
        department = self.departments.get(department_id)

        if department is None:
            return False
        if department.employees:
            raise ValueError("Нельзя удалить подразделение с сотрудниками.")

        del self.departments[department_id]
        return True

    def register_employee(self, employee, branch_id: str | None = None):
        """Регистрирует сотрудника и при необходимости назначает филиал."""
        self.employee_registry.register(employee)

        if branch_id is not None:
            branch = self.get_branch(branch_id)

            if branch is None:
                self.employee_registry.unregister(employee.employee_id)
                raise ValueError("Филиал не найден.")

            branch.add_employee(employee)

    def register_customer(self, customer):
        """Регистрирует нового клиента компании."""
        self.customer_registry.register(customer)

    def register_order(self, order):
        """Регистрирует заказ после проверки клиента."""
        customer = self.customer_registry.get_customer(order.customer.customer_id)

        if customer is not order.customer:
            raise InvalidCustomerError("Заказ принадлежит незарегистрированному клиенту.")

        self.order_registry.register(order)

    def add_vehicle(self, vehicle, branch_id: str | None = None):
        """Добавляет транспорт в автопарк и при необходимости в филиал."""
        self.fleet.add_vehicle(vehicle)

        if branch_id is not None:
            branch = self.get_branch(branch_id)

            if branch is None:
                self.fleet.remove_vehicle(vehicle.vehicle_id)
                raise ValueError("Филиал не найден.")

            branch.add_vehicle(vehicle)

    def add_policy(self, policy: CompanyPolicy):
        """Добавляет внутреннее правило компании."""
        if policy.policy_id in self.policies:
            raise ValueError("Такое правило уже существует.")

        self.policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str):
        """Удаляет правило компании."""
        if policy_id not in self.policies:
            return False

        del self.policies[policy_id]
        return True

    def validate_order_by_policies(self, order):
        """Проверяет заказ по всем действующим правилам."""
        all_violations = []

        for policy in self.policies.values():
            if policy.is_effective():
                violations = policy.validate_order(order)

                for violation in violations:
                    all_violations.append(f"{policy.title}: {violation}")

        return all_violations

    def approve_order(self, order_id: str):
        """Проверяет заказ по правилам компании и переводит его на согласование."""
        order = self.order_registry.get_order(order_id)

        if order is None:
            raise InvalidOrderStatusError("Заказ не найден.")

        violations = self.validate_order_by_policies(order)

        if violations:
            raise InvalidOrderStatusError("Заказ не прошёл проверку: " + "; ".join(violations))

        order.submit_for_approval()

    def assign_order_to_trip(self, order_id: str, trip):
        """Назначает заказ на поездку и регистрирует поездку в автопарке."""
        order = self.order_registry.get_order(order_id)

        if order is None:
            raise InvalidOrderStatusError("Заказ не найден.")
        if trip.vehicle.vehicle_id not in self.fleet.vehicles:
            raise InvalidVehicleError("Транспорт поездки не входит в автопарк компании.")

        order.assign_trip(trip)
        self.fleet.register_trip(trip)

    def transfer_employee(
        self,
        employee_id: str,
        old_branch_id: str,
        new_branch_id: str,
    ):
        """Переводит сотрудника из одного филиала в другой."""
        employee = self.employee_registry.get_employee(employee_id)
        old_branch = self.get_branch(old_branch_id)
        new_branch = self.get_branch(new_branch_id)

        if employee is None:
            raise InvalidDriverError("Сотрудник не найден.")
        if old_branch is None or new_branch is None:
            raise ValueError("Один из филиалов не найден.")
        if employee not in old_branch.employees:
            raise ValueError("Сотрудник не числится в исходном филиале.")
        if not new_branch.is_active:
            raise ValueError("Нельзя перевести сотрудника в закрытый филиал.")

        old_branch.remove_employee(employee)
        new_branch.add_employee(employee)

    def calculate_total_vehicle_capacity(self):
        """Возвращает общую грузоподъёмность автопарка компании."""
        return self.fleet.calculate_total_capacity()

    def calculate_active_employee_count(self):
        """Считает количество работающих сотрудников."""
        return len(self.employee_registry.get_active_employees())

    def calculate_branch_count(self):
        """Считает количество активных филиалов."""
        return sum(1 for branch in self.branches.values() if branch.is_active)

    def calculate_total_warehouse_capacity(self):
        """Считает общую вместимость всех складов компании."""
        total = 0.0

        for branch in self.branches.values():
            total += sum(warehouse.capacity_kg for warehouse in branch.warehouses)

        return round(total, 2)

    def get_available_vehicles(self):
        """Возвращает все свободные транспортные средства компании."""
        return self.fleet.get_available_vehicles()

    def get_active_orders(self):
        """Возвращает заказы, которые ещё выполняются."""
        return [
            order
            for order in self.order_registry.orders.values()
            if order.status not in ("delivered", "cancelled")
        ]

    def get_company_summary(self):
        """Формирует общую сводку о состоянии компании."""
        return {
            "company_id": self.company_id,
            "name": self.name,
            "branches": self.calculate_branch_count(),
            "departments": len(self.departments),
            "employees": self.calculate_active_employee_count(),
            "customers": self.customer_registry.count_customers(),
            "vehicles": len(self.fleet.vehicles),
            "available_vehicles": len(self.get_available_vehicles()),
            "orders": self.order_registry.count_orders(),
            "active_orders": len(self.get_active_orders()),
            "total_vehicle_capacity_kg": (self.calculate_total_vehicle_capacity()),
            "warehouse_capacity_kg": (self.calculate_total_warehouse_capacity()),
        }

    def add_financial_report(self, report):
        """Сохраняет финансовый отчёт компании."""
        if report in self.financial_reports:
            raise ValueError("Отчёт уже добавлен.")

        self.financial_reports.append(report)

    def get_latest_financial_report(self):
        """Возвращает последний созданный финансовый отчёт."""
        if not self.financial_reports:
            return None

        return max(
            self.financial_reports,
            key=lambda report: report.created_at,
        )

    def activate(self):
        """Активирует компанию."""
        self.is_active = True

    def deactivate(self):
        """Отключает компанию, если нет активных поездок."""
        active_trips = [trip for trip in self.fleet.trip_history if trip.status == "in_progress"]

        if active_trips:
            raise DeliveryError("Нельзя отключить компанию во время активных поездок.")

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание к компании."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)