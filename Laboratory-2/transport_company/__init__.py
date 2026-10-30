"""Пакет классов системы управления транспортной компанией."""

# Исключения
from .exceptions import (
    TransportCompanyError,
    InvalidCustomerError,
    InvalidDriverError,
    InvalidVehicleError,
    VehicleUnavailableError,
    DriverUnavailableError,
    InvalidCargoError,
    CargoCapacityExceededError,
    InvalidRouteError,
    InvalidOrderStatusError,
    PaymentError,
    DeliveryError,
)

# Люди
from .people import (
    Person,
    Customer,
    CorporateCustomer,
    IndividualCustomer,
    Employee,
    Driver,
    Dispatcher,
    Manager,
)

# Транспорт
from .vehicles import (
    Vehicle,
    Truck,
    Van,
    RefrigeratedTruck,
    Tanker,
    FlatbedTruck,
    Trailer,
    VehicleInspection,
    MaintenanceRecord,
    FuelRecord,
)

# Грузы
from .cargo import (
    Cargo,
    PerishableCargo,
    FragileCargo,
    DangerousCargo,
    OversizedCargo,
    CargoPackage,
    CargoDocument,
)

# Перевозки
from .transport import (
    RoutePoint,
    Route,
    OrderItem,
    TransportOrder,
    Shipment,
    Stop,
    Trip,
    Delivery,
    Schedule,
)

# Финансы
from .finance import (
    Payment,
    Invoice,
    Transaction,
    Expense,
    Budget,
    SalaryPayment,
    FinancialReport,
)

# Управление компанией
from .company import (
    EmployeeRegistry,
    CustomerRegistry,
    OrderRegistry,
    Fleet,
    Warehouse,
    Department,
    Branch,
    CompanyPolicy,
    TransportCompany,
)

__all__ = [
    # Исключения
    "TransportCompanyError",
    "InvalidCustomerError",
    "InvalidDriverError",
    "InvalidVehicleError",
    "VehicleUnavailableError",
    "DriverUnavailableError",
    "InvalidCargoError",
    "CargoCapacityExceededError",
    "InvalidRouteError",
    "InvalidOrderStatusError",
    "PaymentError",
    "DeliveryError",
    # Люди
    "Person",
    "Customer",
    "CorporateCustomer",
    "IndividualCustomer",
    "Employee",
    "Driver",
    "Dispatcher",
    "Manager",
    # Транспорт
    "Vehicle",
    "Truck",
    "Van",
    "RefrigeratedTruck",
    "Tanker",
    "FlatbedTruck",
    "Trailer",
    "VehicleInspection",
    "MaintenanceRecord",
    "FuelRecord",
    # Грузы
    "Cargo",
    "PerishableCargo",
    "FragileCargo",
    "DangerousCargo",
    "OversizedCargo",
    "CargoPackage",
    "CargoDocument",
    # Перевозки
    "RoutePoint",
    "Route",
    "OrderItem",
    "TransportOrder",
    "Shipment",
    "Stop",
    "Trip",
    "Delivery",
    "Schedule",
    # Финансы
    "Payment",
    "Invoice",
    "Transaction",
    "Expense",
    "Budget",
    "SalaryPayment",
    "FinancialReport",
    # Управление компанией
    "EmployeeRegistry",
    "CustomerRegistry",
    "OrderRegistry",
    "Fleet",
    "Warehouse",
    "Department",
    "Branch",
    "CompanyPolicy",
    "TransportCompany",
]
