"""Application services; independent from the console presentation."""
from dataclasses import dataclass, field
from .exceptions import DuplicateReferenceError, InvalidOrderError, CustomerNotFoundError

@dataclass
class EmployeeRecord:
    employee_id: str
    name: str
    role: str
    active: bool = True

@dataclass
class ShipmentRecord:
    shipment_id: str
    destination: str
    weight_kg: float
    status: str = "registered"

@dataclass
class TransportCompany:
    employees: dict[str, EmployeeRecord] = field(default_factory=dict)
    shipments: dict[str, ShipmentRecord] = field(default_factory=dict)

    def add_employee(self, employee_id: str, name: str, role: str) -> EmployeeRecord:
        employee_id, name, role = employee_id.strip(), name.strip(), role.strip()
        if not employee_id or not name or not role:
            raise ValueError("ID, имя и должность обязательны.")
        if employee_id in self.employees:
            raise DuplicateReferenceError(f"Сотрудник {employee_id} уже существует.")
        employee = EmployeeRecord(employee_id, name, role)
        self.employees[employee_id] = employee
        return employee

    def remove_employee(self, employee_id: str) -> None:
        employee = self.employees.get(employee_id)
        if employee is None:
            raise CustomerNotFoundError(f"Сотрудник {employee_id} не найден.")
        del self.employees[employee_id]

    def register_shipment(self, shipment_id: str, destination: str, weight_kg: float) -> ShipmentRecord:
        shipment_id, destination = shipment_id.strip(), destination.strip()
        if not shipment_id or not destination or weight_kg <= 0:
            raise InvalidOrderError("Нужны номер, адрес назначения и положительный вес.")
        if shipment_id in self.shipments:
            raise DuplicateReferenceError(f"Отправление {shipment_id} уже существует.")
        shipment = ShipmentRecord(shipment_id, destination, float(weight_kg))
        self.shipments[shipment_id] = shipment
        return shipment

    def dispatch_shipment(self, shipment_id: str) -> ShipmentRecord:
        shipment = self.shipments.get(shipment_id)
        if shipment is None:
            raise InvalidOrderError(f"Отправление {shipment_id} не найдено.")
        if shipment.status != "registered":
            raise InvalidOrderError("Отправление можно отправить только один раз.")
        shipment.status = "in_transit"
        return shipment

    def build_report(self) -> str:
        employees = len(self.employees)
        shipments = len(self.shipments)
        in_transit = sum(item.status == "in_transit" for item in self.shipments.values())
        total_weight = sum(item.weight_kg for item in self.shipments.values())
        return (f"Сотрудников: {employees}; отправлений: {shipments}; "
                f"в пути: {in_transit}; общий вес: {total_weight:.2f} кг")
