from datetime import date

from ..exceptions import (
    DeliveryError,
    InvalidVehicleError,
    VehicleUnavailableError,
)
from .Warehouse import Warehouse


class Branch:
    """Филиал транспортной компании."""

    def __init__(
        self,
        branch_id: str,
        name: str,
        address: str,
        phone: str,
        region: str = "",
        manager=None,
    ):
        if not branch_id or not name or not address:
            raise ValueError("Не заполнены основные данные филиала.")

        self.branch_id = branch_id
        self.name = name
        self.address = address
        self.phone = phone
        self.region = region
        self.manager = manager
        self.employees = []
        self.vehicles = []
        self.warehouses = []
        self.is_active = True
        self.opening_date = date.today()
        self.monthly_target = 0.0
        self.notes = []

    def add_employee(self, employee):
        """Добавляет сотрудника в филиал."""
        if employee in self.employees:
            raise ValueError("Сотрудник уже работает в филиале.")

        self.employees.append(employee)

    def remove_employee(self, employee):
        """Удаляет сотрудника из филиала."""
        if employee not in self.employees:
            return False

        self.employees.remove(employee)

        if self.manager is employee:
            self.manager = None

        return True

    def assign_manager(self, manager):
        """Назначает управляющего филиалом."""
        if manager not in self.employees:
            raise ValueError("Управляющий должен числиться в этом филиале.")

        self.manager = manager

    def add_vehicle(self, vehicle):
        """Закрепляет транспортное средство за филиалом."""
        if not vehicle.is_available:
            raise VehicleUnavailableError("Нельзя закрепить занятый транспорт.")
        if vehicle in self.vehicles:
            raise InvalidVehicleError("Транспорт уже закреплён за филиалом.")

        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        """Убирает транспорт из филиала."""
        if vehicle not in self.vehicles:
            return False
        if not vehicle.is_available:
            raise VehicleUnavailableError("Нельзя убрать транспорт во время поездки.")

        self.vehicles.remove(vehicle)
        return True

    def add_warehouse(self, warehouse: Warehouse):
        """Добавляет склад в структуру филиала."""
        if warehouse in self.warehouses:
            raise ValueError("Склад уже добавлен в филиал.")

        self.warehouses.append(warehouse)

    def remove_warehouse(self, warehouse_id: str):
        """Удаляет пустой склад из филиала."""
        for warehouse in self.warehouses:
            if warehouse.warehouse_id == warehouse_id:
                if warehouse.cargos:
                    raise DeliveryError("Нельзя удалить склад с хранящимися грузами.")

                self.warehouses.remove(warehouse)
                return True

        return False

    def find_employee(self, employee_id: str):
        """Находит сотрудника филиала."""
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def calculate_fleet_capacity(self):
        """Считает грузоподъёмность транспорта филиала."""
        return round(
            sum(vehicle.capacity_kg for vehicle in self.vehicles),
            2,
        )

    def calculate_available_capacity(self):
        """Считает грузоподъёмность свободного транспорта."""
        return round(
            sum(vehicle.capacity_kg for vehicle in self.vehicles if vehicle.is_available),
            2,
        )

    def calculate_payroll(self):
        """Считает фонд оплаты труда филиала."""
        return round(
            sum(getattr(employee, "salary", 0) for employee in self.employees),
            2,
        )

    def can_accept_order(self, order):
        """Проверяет, способен ли филиал обслужить заказ по весу."""
        if not self.is_active:
            return False

        return order.total_weight() <= self.calculate_available_capacity()

    def set_monthly_target(self, target: float):
        """Устанавливает план филиала."""
        if target < 0:
            raise ValueError("План не может быть отрицательным.")

        self.monthly_target = round(float(target), 2)

    def activate(self):
        """Активирует филиал."""
        self.is_active = True

    def deactivate(self):
        """Деактивирует филиал, если в нём нет занятых машин."""
        if any(not vehicle.is_available for vehicle in self.vehicles):
            raise VehicleUnavailableError("Нельзя закрыть филиал с работающим транспортом.")

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание к филиалу."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)