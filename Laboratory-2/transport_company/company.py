
"""Управление транспортной компанией."""

from datetime import date, datetime

from exceptions import (
    InvalidCustomerError,
    InvalidDriverError,
    InvalidVehicleError,
    VehicleUnavailableError,
    InvalidOrderStatusError,
    DeliveryError,
)


class EmployeeRegistry:
    """Реестр сотрудников транспортной компании."""

    def __init__(self):
        self.employees = {}
        self.registration_history = []
        self.last_updated = datetime.now()

    def register(self, employee):
        """Регистрирует нового сотрудника."""
        employee_id = getattr(employee, "employee_id", None)

        if not employee_id:
            raise InvalidDriverError("У сотрудника отсутствует идентификатор.")
        if employee_id in self.employees:
            raise InvalidDriverError("Сотрудник уже зарегистрирован.")

        self.employees[employee_id] = employee
        self.registration_history.append(
            f"Зарегистрирован сотрудник {employee_id}"
        )
        self.last_updated = datetime.now()

    def unregister(self, employee_id: str):
        """Удаляет сотрудника из реестра."""
        employee = self.employees.get(employee_id)

        if employee is None:
            return False

        if getattr(employee, "assigned_vehicle", None) is not None:
            raise InvalidDriverError(
                "Нельзя удалить водителя с назначенным транспортом."
            )

        del self.employees[employee_id]
        self.registration_history.append(
            f"Удалён сотрудник {employee_id}"
        )
        self.last_updated = datetime.now()
        return True

    def get_employee(self, employee_id: str):
        """Находит сотрудника по идентификатору."""
        return self.employees.get(employee_id)

    def find_by_name(self, name: str):
        """Ищет сотрудников по имени."""
        search_name = name.lower()

        return [
            employee
            for employee in self.employees.values()
            if search_name in employee.name.lower()
        ]

    def get_active_employees(self):
        """Возвращает список активных сотрудников."""
        return [
            employee
            for employee in self.employees.values()
            if getattr(employee, "is_active", True)
        ]

    def get_drivers(self):
        """Возвращает сотрудников, являющихся водителями."""
        return [
            employee
            for employee in self.employees.values()
            if hasattr(employee, "license_category")
        ]

    def get_by_department(self, department_name: str):
        """Возвращает сотрудников выбранного отдела."""
        return [
            employee
            for employee in self.employees.values()
            if getattr(employee, "department", None) == department_name
        ]

    def change_employee_status(self, employee_id: str, active: bool):
        """Активирует или деактивирует сотрудника."""
        employee = self.get_employee(employee_id)

        if employee is None:
            raise InvalidDriverError("Сотрудник не найден.")

        if active:
            employee.activate()
        else:
            employee.deactivate()

        self.last_updated = datetime.now()

    def calculate_total_salary(self):
        """Считает сумму зарплат всех сотрудников."""
        return round(
            sum(
                getattr(employee, "salary", 0)
                for employee in self.employees.values()
            ),
            2,
        )

    def count_employees(self):
        """Возвращает общее количество сотрудников."""
        return len(self.employees)

    def get_employee_ids(self):
        """Возвращает идентификаторы всех сотрудников."""
        return list(self.employees.keys())

    def clear_inactive(self):
        """Удаляет из реестра всех неактивных сотрудников."""
        inactive_ids = [
            employee_id
            for employee_id, employee in self.employees.items()
            if not getattr(employee, "is_active", True)
            and getattr(employee, "assigned_vehicle", None) is None
        ]

        for employee_id in inactive_ids:
            del self.employees[employee_id]

        self.last_updated = datetime.now()
        return len(inactive_ids)


class CustomerRegistry:
    """Реестр клиентов транспортной компании."""

    def __init__(self):
        self.customers = {}
        self.registration_history = []
        self.last_updated = datetime.now()

    def register(self, customer):
        """Добавляет нового клиента."""
        customer_id = getattr(customer, "customer_id", None)

        if not customer_id:
            raise InvalidCustomerError(
                "У клиента отсутствует идентификатор."
            )
        if customer_id in self.customers:
            raise InvalidCustomerError("Клиент уже зарегистрирован.")

        self.customers[customer_id] = customer
        self.registration_history.append(
            f"Зарегистрирован клиент {customer_id}"
        )
        self.last_updated = datetime.now()

    def unregister(self, customer_id: str):
        """Удаляет клиента, у которого нет активных заказов."""
        customer = self.customers.get(customer_id)

        if customer is None:
            return False

        active_orders = [
            order
            for order in getattr(customer, "orders", [])
            if getattr(order, "status", None)
            not in ("delivered", "cancelled")
        ]

        if active_orders:
            raise InvalidCustomerError(
                "Нельзя удалить клиента с активными заказами."
            )

        del self.customers[customer_id]
        self.registration_history.append(
            f"Удалён клиент {customer_id}"
        )
        self.last_updated = datetime.now()
        return True

    def get_customer(self, customer_id: str):
        """Находит клиента по идентификатору."""
        return self.customers.get(customer_id)

    def find_by_name(self, name: str):
        """Ищет клиентов по имени или названию организации."""
        search_name = name.lower()

        return [
            customer
            for customer in self.customers.values()
            if search_name in customer.name.lower()
        ]

    def get_active_customers(self):
        """Возвращает список активных клиентов."""
        return [
            customer
            for customer in self.customers.values()
            if getattr(customer, "is_active", True)
        ]

    def get_corporate_customers(self):
        """Возвращает корпоративных клиентов."""
        return [
            customer
            for customer in self.customers.values()
            if hasattr(customer, "company_name")
        ]

    def get_customers_with_orders(self):
        """Возвращает клиентов, у которых есть заказы."""
        return [
            customer
            for customer in self.customers.values()
            if getattr(customer, "orders", [])
        ]

    def get_customers_without_orders(self):
        """Возвращает клиентов без заказов."""
        return [
            customer
            for customer in self.customers.values()
            if not getattr(customer, "orders", [])
        ]

    def count_customers(self):
        """Возвращает количество зарегистрированных клиентов."""
        return len(self.customers)

    def calculate_total_orders(self):
        """Считает общее количество заказов клиентов."""
        return sum(
            len(getattr(customer, "orders", []))
            for customer in self.customers.values()
        )

    def get_customer_order_history(self, customer_id: str):
        """Возвращает историю заказов конкретного клиента."""
        customer = self.get_customer(customer_id)

        if customer is None:
            raise InvalidCustomerError("Клиент не найден.")

        return list(getattr(customer, "orders", []))

    def update_status(self, customer_id: str, active: bool):
        """Изменяет активность клиента."""
        customer = self.get_customer(customer_id)

        if customer is None:
            raise InvalidCustomerError("Клиент не найден.")

        if active:
            customer.activate()
        else:
            customer.deactivate()

        self.last_updated = datetime.now()


class OrderRegistry:
    """Реестр транспортных заказов."""

    def __init__(self):
        self.orders = {}
        self.registration_history = []
        self.last_updated = datetime.now()

    def register(self, order):
        """Регистрирует транспортный заказ."""
        order_id = getattr(order, "order_id", None)

        if not order_id:
            raise InvalidOrderStatusError(
                "У заказа отсутствует идентификатор."
            )
        if order_id in self.orders:
            raise InvalidOrderStatusError("Заказ уже зарегистрирован.")

        self.orders[order_id] = order
        self.registration_history.append(
            f"Зарегистрирован заказ {order_id}"
        )
        self.last_updated = datetime.now()

    def unregister(self, order_id: str):
        """Удаляет новый или отменённый заказ из реестра."""
        order = self.orders.get(order_id)

        if order is None:
            return False

        if order.status not in ("new", "cancelled"):
            raise InvalidOrderStatusError(
                "Нельзя удалить заказ в работе."
            )

        del self.orders[order_id]
        self.last_updated = datetime.now()
        return True

    def get_order(self, order_id: str):
        """Находит заказ по идентификатору."""
        return self.orders.get(order_id)

    def get_by_status(self, status: str):
        """Возвращает заказы с указанным статусом."""
        return [
            order
            for order in self.orders.values()
            if order.status == status
        ]

    def get_by_customer(self, customer):
        """Возвращает заказы конкретного клиента."""
        return [
            order
            for order in self.orders.values()
            if order.customer is customer
        ]

    def get_by_priority(self, priority: str):
        """Возвращает заказы с указанным приоритетом."""
        return [
            order
            for order in self.orders.values()
            if order.priority == priority
        ]

    def get_overdue_orders(self, check_date: date | None = None):
        """Находит заказы, срок доставки которых истёк."""
        check_date = check_date or date.today()

        return [
            order
            for order in self.orders.values()
            if order.requested_delivery_date is not None
            and order.requested_delivery_date < check_date
            and order.status not in ("delivered", "cancelled")
        ]

    def calculate_total_weight(self):
        """Считает общий вес всех зарегистрированных заказов."""
        return round(
            sum(order.total_weight() for order in self.orders.values()),
            2,
        )

    def calculate_total_value(self):
        """Считает общую стоимость позиций всех заказов."""
        return round(
            sum(
                order.calculate_items_cost()
                for order in self.orders.values()
            ),
            2,
        )

    def count_orders(self):
        """Возвращает количество зарегистрированных заказов."""
        return len(self.orders)

    def count_by_status(self, status: str):
        """Считает количество заказов с указанным статусом."""
        return len(self.get_by_status(status))

    def cancel_order(self, order_id: str):
        """Отменяет заказ, если это допускает его текущий статус."""
        order = self.get_order(order_id)

        if order is None:
            raise InvalidOrderStatusError("Заказ не найден.")

        order.cancel()
        self.last_updated = datetime.now()

    def get_orders_for_period(
        self,
        start_date: date,
        end_date: date,
    ):
        """Возвращает заказы, созданные в указанном периоде."""
        if end_date < start_date:
            raise ValueError("Некорректный период.")

        return [
            order
            for order in self.orders.values()
            if start_date <= order.created_at.date() <= end_date
        ]

    def get_order_statistics(self):
        """Формирует статистику по статусам заказов."""
        statistics = {}

        for order in self.orders.values():
            statistics[order.status] = (
                statistics.get(order.status, 0) + 1
            )

        return statistics


class Fleet:
    """Автопарк транспортной компании."""

    def __init__(
        self,
        fleet_id: str,
        name: str,
        max_vehicle_count: int = 100,
    ):
        if not fleet_id or not name:
            raise ValueError("Не указаны идентификатор или название автопарка.")
        if max_vehicle_count <= 0:
            raise ValueError("Размер автопарка должен быть положительным.")

        self.fleet_id = fleet_id
        self.name = name
        self.max_vehicle_count = max_vehicle_count
        self.vehicles = {}
        self.assigned_drivers = {}
        self.trip_history = []
        self.maintenance_records = []
        self.is_active = True
        self.notes = []

    def add_vehicle(self, vehicle):
        """Добавляет транспортное средство в автопарк."""
        vehicle_id = getattr(vehicle, "vehicle_id", None)

        if not vehicle_id:
            raise InvalidVehicleError("У транспорта отсутствует идентификатор.")
        if vehicle_id in self.vehicles:
            raise InvalidVehicleError("Транспорт уже есть в автопарке.")
        if len(self.vehicles) >= self.max_vehicle_count:
            raise InvalidVehicleError("Достигнут лимит автопарка.")

        self.vehicles[vehicle_id] = vehicle

    def remove_vehicle(self, vehicle_id: str):
        """Удаляет свободное транспортное средство."""
        vehicle = self.vehicles.get(vehicle_id)

        if vehicle is None:
            return False
        if not vehicle.is_available:
            raise VehicleUnavailableError(
                "Нельзя удалить используемое транспортное средство."
            )

        for driver_id, driver in list(self.assigned_drivers.items()):
            if getattr(driver, "assigned_vehicle", None) is vehicle:
                raise InvalidVehicleError(
                    "Сначала необходимо отвязать водителя от транспорта."
                )

        del self.vehicles[vehicle_id]
        return True

    def get_vehicle(self, vehicle_id: str):
        """Находит транспорт по идентификатору."""
        return self.vehicles.get(vehicle_id)

    def get_available_vehicles(self):
        """Возвращает свободный транспорт."""
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if vehicle.is_available
        ]

    def get_unavailable_vehicles(self):
        """Возвращает занятый или недоступный транспорт."""
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if not vehicle.is_available
        ]

    def find_by_registration(self, registration_number: str):
        """Находит транспорт по регистрационному номеру."""
        for vehicle in self.vehicles.values():
            if vehicle.registration_number == registration_number:
                return vehicle

        return None

    def assign_driver(self, driver, vehicle_id: str):
        """Назначает водителя на транспортное средство."""
        vehicle = self.get_vehicle(vehicle_id)

        if vehicle is None:
            raise InvalidVehicleError("Транспорт не найден.")
        if not vehicle.is_available:
            raise VehicleUnavailableError("Транспорт уже занят.")

        driver_id = getattr(driver, "employee_id", None)

        if not driver_id:
            raise InvalidDriverError("У водителя отсутствует идентификатор.")
        if driver_id in self.assigned_drivers:
            raise InvalidDriverError("Водитель уже числится в автопарке.")

        driver.assign_vehicle(vehicle)
        self.assigned_drivers[driver_id] = driver

    def unassign_driver(self, driver_id: str):
        """Отвязывает водителя от транспортного средства."""
        driver = self.assigned_drivers.get(driver_id)

        if driver is None:
            return False
        if not driver.is_available:
            raise InvalidDriverError(
                "Нельзя отвязать водителя во время поездки."
            )

        driver.assigned_vehicle = None
        del self.assigned_drivers[driver_id]
        return True

    def register_trip(self, trip):
        """Добавляет поездку в историю автопарка."""
        if trip.vehicle.vehicle_id not in self.vehicles:
            raise InvalidVehicleError(
                "Транспорт поездки не принадлежит этому автопарку."
            )
        if trip in self.trip_history:
            raise ValueError("Поездка уже зарегистрирована.")

        self.trip_history.append(trip)

    def get_vehicle_trips(self, vehicle_id: str):
        """Возвращает поездки конкретного автомобиля."""
        return [
            trip
            for trip in self.trip_history
            if trip.vehicle.vehicle_id == vehicle_id
        ]

    def get_vehicles_by_fuel(self, fuel_type: str):
        """Фильтрует транспорт по типу топлива."""
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if vehicle.fuel_type == fuel_type
        ]

    def calculate_total_capacity(self):
        """Считает суммарную грузоподъёмность автопарка."""
        return round(
            sum(
                vehicle.capacity_kg
                for vehicle in self.vehicles.values()
            ),
            2,
        )

    def calculate_average_mileage(self):
        """Вычисляет средний пробег транспортных средств."""
        if not self.vehicles:
            return 0.0

        return round(
            sum(
                vehicle.mileage_km
                for vehicle in self.vehicles.values()
            ) / len(self.vehicles),
            2,
        )

    def get_vehicles_needing_inspection(self):
        """Находит автомобили, которым нужна проверка."""
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if vehicle.needs_inspection()
        ]

    def add_maintenance_record(self, record):
        """Сохраняет запись о техническом обслуживании."""
        if record.vehicle.vehicle_id not in self.vehicles:
            raise InvalidVehicleError(
                "Транспорт не принадлежит этому автопарку."
            )

        self.maintenance_records.append(record)

    def activate(self):
        """Активирует автопарк."""
        self.is_active = True

    def deactivate(self):
        """Отключает автопарк для новых назначений."""
        if self.get_unavailable_vehicles():
            raise VehicleUnavailableError(
                "Нельзя отключить автопарк с занятыми автомобилями."
            )

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание к автопарку."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)


class Warehouse:
    """Склад для временного хранения грузов."""

    def __init__(
        self,
        warehouse_id: str,
        name: str,
        address: str,
        capacity_kg: float,
        manager=None,
    ):
        if not warehouse_id or not name or not address:
            raise ValueError("Не заполнены данные склада.")
        if capacity_kg <= 0:
            raise ValueError("Вместимость склада должна быть положительной.")

        self.warehouse_id = warehouse_id
        self.name = name
        self.address = address
        self.capacity_kg = float(capacity_kg)
        self.used_capacity_kg = 0.0
        self.reserved_capacity_kg = 0.0
        self.manager = manager
        self.cargos = {}
        self.is_open = True
        self.opening_date = date.today()
        self.notes = []

    def store_cargo(self, cargo):
        """Размещает груз на складе."""
        cargo_id = getattr(cargo, "cargo_id", None)

        if not self.is_open:
            raise DeliveryError("Склад закрыт.")
        if not cargo_id:
            raise DeliveryError("У груза отсутствует идентификатор.")
        if cargo_id in self.cargos:
            raise DeliveryError("Груз уже находится на складе.")
        if self.get_free_capacity() < cargo.weight_kg:
            raise DeliveryError("Недостаточно свободного места на складе.")

        self.cargos[cargo_id] = cargo
        self.used_capacity_kg += cargo.weight_kg

    def release_cargo(self, cargo_id: str):
        """Выдаёт груз со склада."""
        cargo = self.cargos.get(cargo_id)

        if cargo is None:
            return None

        del self.cargos[cargo_id]
        self.used_capacity_kg = max(
            0.0,
            self.used_capacity_kg - cargo.weight_kg,
        )
        return cargo

    def get_cargo(self, cargo_id: str):
        """Находит груз по идентификатору."""
        return self.cargos.get(cargo_id)

    def find_cargo_by_name(self, name: str):
        """Ищет грузы по названию."""
        search_name = name.lower()

        return [
            cargo
            for cargo in self.cargos.values()
            if search_name in cargo.name.lower()
        ]

    def get_free_capacity(self):
        """Вычисляет свободную вместимость с учётом резерва."""
        return round(
            self.capacity_kg
            - self.used_capacity_kg
            - self.reserved_capacity_kg,
            2,
        )

    def reserve_capacity(self, weight_kg: float):
        """Резервирует место для будущего поступления груза."""
        if weight_kg <= 0:
            raise ValueError("Резервируемый вес должен быть положительным.")
        if weight_kg > self.get_free_capacity():
            raise DeliveryError("Недостаточно места для резерва.")

        self.reserved_capacity_kg += weight_kg

    def cancel_reservation(self, weight_kg: float):
        """Снимает резерв вместимости."""
        if weight_kg <= 0 or weight_kg > self.reserved_capacity_kg:
            raise ValueError("Некорректный размер резерва.")

        self.reserved_capacity_kg -= weight_kg

    def calculate_occupancy(self):
        """Вычисляет процент заполненности склада."""
        if self.capacity_kg == 0:
            return 0.0

        return round(
            self.used_capacity_kg / self.capacity_kg * 100,
            2,
        )

    def get_cargo_count(self):
        """Возвращает количество грузов на складе."""
        return len(self.cargos)

    def get_total_cargo_value(self):
        """Считает суммарную объявленную стоимость грузов."""
        return round(
            sum(
                cargo.declared_value
                for cargo in self.cargos.values()
            ),
            2,
        )

    def has_cargo(self, cargo_id: str):
        """Проверяет наличие груза на складе."""
        return cargo_id in self.cargos

    def change_manager(self, new_manager):
        """Назначает нового управляющего складом."""
        if new_manager is None:
            raise ValueError("Необходимо указать управляющего.")

        self.manager = new_manager

    def open_warehouse(self):
        """Открывает склад."""
        self.is_open = True

    def close_warehouse(self):
        """Закрывает склад для новых операций."""
        if self.cargos:
            raise DeliveryError(
                "Нельзя закрыть склад, пока на нём остаются грузы."
            )

        self.is_open = False

    def add_note(self, note: str):
        """Добавляет примечание к складу."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)


class Department:
    """Подразделение транспортной компании."""

    def __init__(
        self,
        department_id: str,
        name: str,
        description: str = "",
        manager=None,
        monthly_target: float = 0.0,
    ):
        if not department_id or not name:
            raise ValueError("Не указаны данные подразделения.")
        if monthly_target < 0:
            raise ValueError("План подразделения не может быть отрицательным.")

        self.department_id = department_id
        self.name = name
        self.description = description
        self.manager = manager
        self.employees = []
        self.budget = 0.0
        self.monthly_target = monthly_target
        self.expenses = []
        self.is_active = True
        self.creation_date = date.today()
        self.notes = []

    def add_employee(self, employee):
        """Добавляет сотрудника в подразделение."""
        if employee in self.employees:
            raise ValueError("Сотрудник уже находится в подразделении.")

        self.employees.append(employee)
        employee.department = self.name

    def remove_employee(self, employee):
        """Удаляет сотрудника из подразделения."""
        if employee not in self.employees:
            return False

        self.employees.remove(employee)
        employee.department = None

        if self.manager is employee:
            self.manager = None

        return True

    def assign_manager(self, manager):
        """Назначает руководителя подразделения."""
        if manager not in self.employees:
            raise ValueError(
                "Руководитель должен быть сотрудником подразделения."
            )

        self.manager = manager

    def change_manager(self, new_manager):
        """Меняет руководителя подразделения."""
        return self.assign_manager(new_manager)

    def set_budget(self, amount: float):
        """Устанавливает бюджет подразделения."""
        if amount < 0:
            raise ValueError("Бюджет не может быть отрицательным.")

        self.budget = round(float(amount), 2)

    def add_expense(self, expense):
        """Добавляет расход подразделения."""
        if expense not in self.expenses:
            self.expenses.append(expense)

    def calculate_expenses(self):
        """Считает подтверждённые расходы подразделения."""
        return round(
            sum(
                expense.amount
                for expense in self.expenses
                if expense.status in ("approved", "reimbursed")
            ),
            2,
        )

    def calculate_remaining_budget(self):
        """Вычисляет остаток бюджета."""
        return round(self.budget - self.calculate_expenses(), 2)

    def calculate_payroll(self):
        """Считает сумму зарплат сотрудников подразделения."""
        return round(
            sum(
                getattr(employee, "salary", 0)
                for employee in self.employees
            ),
            2,
        )

    def find_employee(self, employee_id: str):
        """Находит сотрудника подразделения по идентификатору."""
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def assign_task(self, employee_id: str, task: str):
        """Передаёт задачу конкретному сотруднику."""
        employee = self.find_employee(employee_id)

        if employee is None:
            raise InvalidDriverError(
                "Сотрудник не найден в этом подразделении."
            )

        if not callable(getattr(employee, "assign_task", None)):
            raise InvalidDriverError(
                "Сотрудник не поддерживает назначение задач."
            )

        employee.assign_task(task)

    def set_monthly_target(self, target: float):
        """Изменяет плановый показатель подразделения."""
        if target < 0:
            raise ValueError("План не может быть отрицательным.")

        self.monthly_target = round(float(target), 2)

    def activate(self):
        """Активирует подразделение."""
        self.is_active = True

    def deactivate(self):
        """Деактивирует подразделение."""
        if self.employees:
            raise ValueError(
                "Перед отключением подразделения необходимо распределить сотрудников."
            )

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание подразделения."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)


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
            raise ValueError(
                "Управляющий должен числиться в этом филиале."
            )

        self.manager = manager

    def add_vehicle(self, vehicle):
        """Закрепляет транспортное средство за филиалом."""
        if not vehicle.is_available:
            raise VehicleUnavailableError(
                "Нельзя закрепить занятый транспорт."
            )
        if vehicle in self.vehicles:
            raise InvalidVehicleError(
                "Транспорт уже закреплён за филиалом."
            )

        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        """Убирает транспорт из филиала."""
        if vehicle not in self.vehicles:
            return False
        if not vehicle.is_available:
            raise VehicleUnavailableError(
                "Нельзя убрать транспорт во время поездки."
            )

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
                    raise DeliveryError(
                        "Нельзя удалить склад с хранящимися грузами."
                    )

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
            sum(
                vehicle.capacity_kg
                for vehicle in self.vehicles
                if vehicle.is_available
            ),
            2,
        )

    def calculate_payroll(self):
        """Считает фонд оплаты труда филиала."""
        return round(
            sum(
                getattr(employee, "salary", 0)
                for employee in self.employees
            ),
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
            raise VehicleUnavailableError(
                "Нельзя закрыть филиал с работающим транспортом."
            )

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание к филиалу."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)


class CompanyPolicy:
    """Правило или внутренний регламент транспортной компании."""

    def __init__(
        self,
        policy_id: str,
        title: str,
        category: str,
        description: str,
        rules: dict | None = None,
        effective_from: date | None = None,
        effective_until: date | None = None,
    ):
        if not policy_id or not title or not category:
            raise ValueError("Не заполнены основные данные правила.")

        self.policy_id = policy_id
        self.title = title
        self.category = category
        self.description = description
        self.rules = dict(rules or {})
        self.effective_from = effective_from or date.today()
        self.effective_until = effective_until
        self.is_enabled = True
        self.applied_count = 0
        self.last_applied_at = None
        self.notes = []

    def set_rule(self, rule_name: str, value):
        """Добавляет новое правило или изменяет существующее."""
        if not self.is_enabled:
            raise ValueError("Нельзя менять отключённое правило.")
        if not rule_name:
            raise ValueError("Название правила не может быть пустым.")

        self.rules[rule_name] = value

    def remove_rule(self, rule_name: str):
        """Удаляет отдельное условие правила."""
        if rule_name not in self.rules:
            return False

        del self.rules[rule_name]
        return True

    def get_rule(self, rule_name: str, default=None):
        """Возвращает значение выбранного условия."""
        return self.rules.get(rule_name, default)

    def is_effective(self, check_date: date | None = None):
        """Проверяет, действует ли правило на выбранную дату."""
        check_date = check_date or date.today()

        if not self.is_enabled:
            return False
        if check_date < self.effective_from:
            return False
        if (
            self.effective_until is not None
            and check_date > self.effective_until
        ):
            return False

        return True

    def validate_order(self, order):
        """Проверяет заказ на соответствие внутренним правилам.

        Возвращает список обнаруженных нарушений.
        Пустой список означает, что нарушений не найдено.
        """
        violations = []
        cargos = [
            item.cargo
            for item in order.items
            for _ in range(item.quantity)
        ]

        max_weight = self.get_rule("max_order_weight_kg")
        if max_weight is not None and order.total_weight() > max_weight:
            violations.append("Превышен максимальный вес заказа.")

        max_items = self.get_rule("max_cargo_items")
        if max_items is not None and len(order.items) > max_items:
            violations.append("В заказе слишком много позиций.")

        max_value = self.get_rule("max_order_value")
        if (
            max_value is not None
            and order.calculate_items_cost() > max_value
        ):
            violations.append("Превышена максимальная стоимость заказа.")

        if self.get_rule("require_packed_cargo", False):
            if any(not cargo.is_packed for cargo in cargos):
                violations.append("Все грузы должны быть упакованы.")

        if not self.get_rule("allow_dangerous_cargo", True):
            if any(hasattr(cargo, "hazard_class") for cargo in cargos):
                violations.append(
                    "Перевозка опасных грузов запрещена правилом."
                )

        if not self.get_rule("allow_oversized_cargo", True):
            if any(hasattr(cargo, "length_m") for cargo in cargos):
                violations.append(
                    "Перевозка негабаритных грузов запрещена правилом."
                )

        minimum_notice_days = self.get_rule("minimum_notice_days")
        if (
            minimum_notice_days is not None
            and order.requested_delivery_date is not None
        ):
            days_notice = (
                order.requested_delivery_date - date.today()
            ).days

            if days_notice < minimum_notice_days:
                violations.append(
                    "Заказ оформлен слишком близко к дате доставки."
                )

        return violations

    def check_order(self, order, check_date: date | None = None):
        """Проверяет заказ с учётом срока действия правила."""
        if not self.is_effective(check_date):
            return False

        return not self.validate_order(order)

    def apply_to_order(self, order):
        """Проверяет заказ и регистрирует применение правила."""
        if not self.is_effective():
            raise InvalidOrderStatusError(
                "Правило не действует на текущую дату."
            )

        violations = self.validate_order(order)

        if violations:
            raise InvalidOrderStatusError(
                "Заказ не соответствует правилам: "
                + "; ".join(violations)
            )

        self.applied_count += 1
        self.last_applied_at = datetime.now()
        return True

    def enable(self):
        """Включает правило."""
        self.is_enabled = True

    def disable(self):
        """Отключает правило."""
        self.is_enabled = False

    def extend_validity(self, new_date: date):
        """Продлевает срок действия правила."""
        if new_date < self.effective_from:
            raise ValueError(
                "Дата окончания не может быть раньше даты начала."
            )
        if (
            self.effective_until is not None
            and new_date < self.effective_until
        ):
            raise ValueError(
                "Продление не должно сокращать срок действия правила."
            )

        self.effective_until = new_date

    def add_note(self, note: str):
        """Добавляет примечание к правилу."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)


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
            raise ValueError(
                "Перед удалением филиала необходимо освободить его ресурсы."
            )

        del self.branches[branch_id]
        return True

    def get_branch(self, branch_id: str):
        """Находит филиал по идентификатору."""
        return self.branches.get(branch_id)

    def add_department(self, department: Department):
        """Добавляет подразделение компании."""
        if department.department_id in self.departments:
            raise ValueError(
                "Подразделение с таким идентификатором уже существует."
            )

        self.departments[department.department_id] = department

    def remove_department(self, department_id: str):
        """Удаляет пустое подразделение."""
        department = self.departments.get(department_id)

        if department is None:
            return False
        if department.employees:
            raise ValueError(
                "Нельзя удалить подразделение с сотрудниками."
            )

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
        customer = self.customer_registry.get_customer(
            order.customer.customer_id
        )

        if customer is not order.customer:
            raise InvalidCustomerError(
                "Заказ принадлежит незарегистрированному клиенту."
            )

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
                    all_violations.append(
                        f"{policy.title}: {violation}"
                    )

        return all_violations

    def approve_order(self, order_id: str):
        """Проверяет заказ по правилам компании и переводит его на согласование."""
        order = self.order_registry.get_order(order_id)

        if order is None:
            raise InvalidOrderStatusError("Заказ не найден.")

        violations = self.validate_order_by_policies(order)

        if violations:
            raise InvalidOrderStatusError(
                "Заказ не прошёл проверку: "
                + "; ".join(violations)
            )

        order.submit_for_approval()

    def assign_order_to_trip(self, order_id: str, trip):
        """Назначает заказ на поездку и регистрирует поездку в автопарке."""
        order = self.order_registry.get_order(order_id)

        if order is None:
            raise InvalidOrderStatusError("Заказ не найден.")
        if trip.vehicle.vehicle_id not in self.fleet.vehicles:
            raise InvalidVehicleError(
                "Транспорт поездки не входит в автопарк компании."
            )

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
        return sum(
            1 for branch in self.branches.values()
            if branch.is_active
        )

    def calculate_total_warehouse_capacity(self):
        """Считает общую вместимость всех складов компании."""
        total = 0.0

        for branch in self.branches.values():
            total += sum(
                warehouse.capacity_kg
                for warehouse in branch.warehouses
            )

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
            "total_vehicle_capacity_kg": (
                self.calculate_total_vehicle_capacity()
            ),
            "warehouse_capacity_kg": (
                self.calculate_total_warehouse_capacity()
            ),
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
        active_trips = [
            trip
            for trip in self.fleet.trip_history
            if trip.status == "in_progress"
        ]

        if active_trips:
            raise DeliveryError(
                "Нельзя отключить компанию во время активных поездок."
            )

        self.is_active = False

    def add_note(self, note: str):
        """Добавляет примечание к компании."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)
