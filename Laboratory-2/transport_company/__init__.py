"""Пакет классов системы управления транспортной компанией.

Можно импортировать классы напрямую из пакета:
    from transport_company import TransportCompany, Driver, Truck

Имя пакета определяется именем папки, в которой лежит этот файл.
"""

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

from .cargo import (
    Cargo,
    PerishableCargo,
    FragileCargo,
    DangerousCargo,
    OversizedCargo,
    CargoPackage,
    CargoDocument,
)

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

from .finance import (
    Payment,
    Invoice,
    Transaction,
    Expense,
    Budget,
    SalaryPayment,
    FinancialReport,
)

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

__all__ = [name for name in globals() if not name.startswith("_")]
