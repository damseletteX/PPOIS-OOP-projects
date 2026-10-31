# Transportation Company — Python OOP Project

A Python object-oriented project that models the core operations of a transportation company. It includes customer and employee management, a vehicle fleet, cargo handling, transport orders, routes and trips, delivery tracking, warehouse operations, payments, invoicing, budgets, and financial reporting.

The project is organised as a Python package (`transport_company`) with a separate console interface (`main.py`). It uses in-memory objects and collections; no database or external service is required.

---

## Features

- Register individual and corporate customers.
- Register employees, drivers, dispatchers, and managers.
- Manage different vehicle types, driver assignments, inspections, maintenance, and fuel records.
- Create and manage regular, perishable, fragile, dangerous, and oversized cargo.
- Create customer transport orders, add cargo items, set priorities and delivery deadlines, and manage order statuses.
- Create routes, stops, trips, schedules, and deliveries.
- Prepare shipments, check loading readiness, load and unload cargo, and record delivery results.
- Issue invoices, process payments, register refunds, and track expenses and budgets.
- Generate financial summaries and company-level operational summaries.
- Apply company policies to validate transport orders.

## Classes by package

The domain model contains **50 classes** distributed across six modules, plus **12 custom exception classes**.

### `people` — Customers and employees

| Class | Main data | Key behaviours |
|---|---|---|
| `Person` | `name`, `phone`, `email`, `is_active` | Update contact details, activate/deactivate a person, return contact information. |
| `Customer` | `address`, `orders`, `discount_percent`, `is_verified` | Add/remove orders, verify a customer, set and calculate discounts, change address. |
| `IndividualCustomer` | `passport_number`, `preferred_contact`, `completed_orders` | Set preferred contact method, record completed orders, identify regular customers, update passport data. |
| `CorporateCustomer` | `tax_number`, `contact_person`, `contract_numbers`, `credit_limit` | Manage contact person and contracts, set a credit limit, check deferred-payment eligibility. |
| `Employee` | `employee_id`, `salary`, `department`, `is_available`, `assigned_tasks` | Assign and complete tasks, change department, calculate annual salary, check work availability. |
| `Driver` | `license_number`, `license_categories`, `experience_years`, `assigned_vehicle`, `completed_trips`, `is_on_trip` | Check licence category, assign a vehicle, start/finish a trip, update licence categories. |
| `Dispatcher` | `managed_trips`, `shift`, `max_trips` | Register and close trips, set a shift, find a managed trip, check dispatch capacity. |
| `Manager` | `managed_customers`, `approved_orders`, `monthly_target`, `monthly_revenue` | Register/remove customers, approve orders, set revenue targets, record revenue, calculate target completion. |

### `vehicles` — Fleet and vehicle operation

| Class | Main data | Key behaviours |
|---|---|---|
| `Vehicle` | `vehicle_id`, `brand`, `model`, `year`, `registration_number`, `capacity_kg`, `fuel_type`, `mileage_km`, `is_available` | Change availability and location, update mileage, check cargo capacity, calculate age, manage inspection, maintenance, and fuel records. |
| `Truck` | `cargo_volume_m3`, `has_crane` | Install/remove a crane, calculate load percentage. |
| `Van` | `cargo_volume_m3`, `has_side_door` | Open or remove the side door. |
| `RefrigeratedTruck` | `min_temperature_c`, `max_temperature_c`, `current_temperature_c`, `cooling_enabled` | Set temperature, enable/disable cooling, check temperature range. |
| `Tanker` | `tank_volume_liters`, `current_volume_liters`, `tank_clean` | Load/unload liquid, clean the tank, mark the tank as dirty. |
| `FlatbedTruck` | `platform_length_m`, `cargo_secured` | Secure/release cargo, check whether cargo length is supported. |
| `Trailer` | `trailer_id`, `registration_number`, `capacity_kg`, `volume_m3`, `attached_vehicle`, `is_attached` | Attach to/detach from a vehicle, check carrying capacity. |
| `VehicleInspection` | `inspection_id`, `vehicle`, `inspection_date`, `inspector`, `passed`, `next_inspection_date` | Conduct an inspection, schedule the next inspection, check whether it is overdue. |
| `MaintenanceRecord` | `record_id`, `vehicle`, `service_date`, `description`, `cost`, `completed`, `parts_used` | Complete service, add used parts, update maintenance cost. |
| `FuelRecord` | `record_id`, `vehicle`, `fuel_date`, `liters`, `price_per_liter`, `total_cost`, `fuel_type` | Calculate fuel cost and update the price per litre. |

### `cargo` — Cargo, packaging, and documents

| Class | Main data | Key behaviours |
|---|---|---|
| `Cargo` | `cargo_id`, `name`, `weight_kg`, `volume_m3`, `declared_value`, `status`, `origin`, `destination`, `packages`, `documents` | Set destination, pack/unpack, insure cargo, update status, calculate density, check vehicle capacity, manage packages and documents. |
| `PerishableCargo` | `expiry_date`, `storage_temperature_c`, `requires_refrigeration`, `temperature_history` | Check expiry, record and validate storage temperature, check refrigerated-vehicle compatibility, calculate days to expiry. |
| `FragileCargo` | `fragility_level`, `requires_special_handling`, `shock_sensitive`, `handling_instructions` | Set handling instructions, assess damage risk, determine whether careful loading is required. |
| `DangerousCargo` | `hazard_class`, `un_number`, `requires_special_permit`, `permit_number`, `emergency_contact`, `safety_instructions` | Set a permit and emergency contact, add safety instructions, check transport requirements. |
| `OversizedCargo` | `length_m`, `width_m`, `height_m`, `permit_number`, `route_restrictions`, `requires_escort` | Calculate geometric volume, manage permits and route restrictions, require an escort, check flatbed compatibility. |
| `CargoPackage` | `package_id`, `package_type`, `weight_kg`, `label`, `is_sealed`, `is_damaged`, `packing_date` | Seal/unseal a package, mark damage, replace a label, check transport readiness. |
| `CargoDocument` | `document_id`, `cargo`, `document_type`, `issue_date`, `expiry_date`, `document_number`, `is_verified` | Verify/revoke verification, check expiry, update document number, add notes. |

### `transport` — Orders, routes, shipments, trips, and deliveries

| Class | Main data | Key behaviours |
|---|---|---|
| `RoutePoint` | `point_id`, `address`, `sequence_number`, `planned_arrival`, `actual_arrival`, `is_completed` | Record arrival, set planned arrival, calculate delay, add a note. |
| `Route` | `route_id`, `name`, `origin`, `destination`, `distance_km`, `points`, `restrictions`, `toll_cost` | Add/remove route points, estimate duration and cost, manage restrictions and active state, find the next point, calculate progress. |
| `OrderItem` | `item_id`, `cargo`, `quantity`, `unit_price`, `special_instructions`, `is_loaded`, `is_unloaded` | Calculate weight, volume, and price; set instructions; mark loading and unloading. |
| `TransportOrder` | `order_id`, `customer`, `origin`, `destination`, `created_at`, `status`, `items`, `route`, `assigned_trip`, `priority`, `requested_delivery_date` | Add/remove items, set route and status, submit/approve/cancel an order, calculate weight/volume/cost, assign a trip, set priority and deadline. |
| `Shipment` | `shipment_id`, `order`, `prepared_date`, `items`, `is_ready`, `loaded_vehicle`, `loading_time`, `unloading_time`, `seal_number` | Check readiness, prepare shipment, load onto and unload from a vehicle, set seal number. |
| `Stop` | `stop_id`, `address`, `purpose`, `planned_time`, `actual_time`, `duration_minutes`, `is_completed` | Schedule and complete a stop, calculate delay, add notes. |
| `Trip` | `trip_id`, `driver`, `vehicle`, `route`, `departure_time`, `arrival_time`, `status`, `orders`, `stops`, `distance_travelled_km` | Add orders/stops, start/finish/cancel a trip, calculate duration and average speed, add notes. |
| `Delivery` | `delivery_id`, `order`, `recipient`, `address`, `scheduled_date`, `status`, `actual_delivery_time`, `received_by`, `proof_of_delivery`, `failure_reason` | Mark in transit, confirm delivery, report failure, reschedule, check lateness, record recipient. |
| `Schedule` | `schedule_id`, `name`, `trips`, `is_active`, `created_at`, `notes` | Add/remove trips, find trips by date or availability, cancel a schedule, add notes. |

### `finance` — Payments, invoices, expenses, and reports

| Class | Main data | Key behaviours |
|---|---|---|
| `Payment` | `payment_id`, `order`, `invoice`, `amount`, `payment_method`, `payment_date`, `status`, `refunded_amount`, `transactions` | Process/fail a payment, refund fully or partially, calculate refundable balance, change payment method, check success. |
| `Invoice` | `invoice_id`, `order`, `issue_date`, `due_date`, `tax_rate`, `discount_amount`, `items`, `additional_charges`, `payments`, `amount_paid`, `status` | Calculate subtotal/tax/total, add charges, apply discount, issue invoice, register payments/refunds, calculate balance, check overdue status, cancel. |
| `Transaction` | `transaction_id`, `payment`, `transaction_type`, `amount`, `timestamp`, `status`, `external_reference` | Mark successful/failed, reverse a transaction, set external reference, identify refunds. |
| `Expense` | `expense_id`, `category`, `description`, `amount`, `expense_date`, `receipt_number`, `status`, `approved_by`, `is_reimbursed` | Approve/reject an expense, mark reimbursement, update amount/category, add notes, check receipt. |
| `Budget` | `budget_id`, `category`, `limit_amount`, `period_start`, `period_end`, `expenses`, `is_active` | Add/remove expenses, calculate spend and remaining balance, check limit, calculate usage percentage, open/close budget. |
| `SalaryPayment` | `salary_payment_id`, `employee`, `period_start`, `period_end`, `base_salary`, `bonus`, `deductions`, `status`, `payment_date` | Calculate net salary, add bonus/deduction, pay or cancel salary, check payment status. |
| `FinancialReport` | `report_id`, `period_start`, `period_end`, `payments`, `expenses`, `salary_payments`, `created_at`, `is_finalized` | Collect financial records, calculate revenue/costs/profit, count payments, finalize report, generate summary. |

### `company` — Company structure and registries

| Class | Main data | Key behaviours |
|---|---|---|
| `EmployeeRegistry` | `employees`, `registration_history`, `last_updated` | Register/unregister employees, search and filter employees, find drivers, change status, calculate payroll, remove inactive employees. |
| `CustomerRegistry` | `customers`, `registration_history`, `last_updated` | Register/unregister customers, search and filter customers, find corporate customers, inspect order history, count orders. |
| `OrderRegistry` | `orders`, `registration_history`, `last_updated` | Register/unregister orders, filter by status/customer/priority, find overdue orders, calculate totals and statistics, cancel orders. |
| `Fleet` | `fleet_id`, `name`, `max_vehicle_count`, `vehicles`, `assigned_drivers`, `trip_history`, `maintenance_records` | Add/remove vehicles, assign drivers, register trips, filter vehicles, calculate fleet capacity and mileage, find vehicles requiring inspection. |
| `Warehouse` | `warehouse_id`, `name`, `address`, `capacity_kg`, `used_capacity_kg`, `reserved_capacity_kg`, `manager`, `cargos` | Store/release cargo, reserve capacity, calculate occupancy and cargo value, open/close warehouse. |
| `Department` | `department_id`, `name`, `manager`, `employees`, `budget`, `monthly_target`, `expenses` | Manage employees and manager, set budget/target, assign tasks, calculate expenses, remaining budget, and payroll. |
| `Branch` | `branch_id`, `name`, `address`, `phone`, `region`, `manager`, `employees`, `vehicles`, `warehouses` | Manage employees, vehicles, warehouses, and manager; calculate fleet capacity and payroll; check ability to accept an order. |
| `CompanyPolicy` | `policy_id`, `title`, `category`, `rules`, `effective_from`, `effective_until`, `is_enabled`, `applied_count` | Set/remove rules, check validity, validate orders, apply/enable/disable policies, extend validity. |
| `TransportCompany` | `company_id`, `name`, `legal_name`, `tax_id`, `branches`, `departments`, `fleet`, registries, `policies`, `financial_reports` | Register company resources, manage branches/departments/policies, validate and approve orders, assign orders to trips, transfer employees, generate company summary. |

---

## Associations

An association is a relationship where one object stores a reference to another object, contains it in a collection, or receives it as a method parameter. The model contains more than 30 such relationships. Examples include:

| From | To | Relationship |
|---|---|---|
| `Customer` | `TransportOrder` | Stores the customer's orders. |
| `TransportOrder` | `Customer` | Identifies the customer who placed the order. |
| `Driver` | `Vehicle` | Holds the assigned vehicle. |
| `Dispatcher` | `Trip` | Maintains managed trips. |
| `Vehicle` | `VehicleInspection` | Stores inspection records. |
| `Vehicle` | `MaintenanceRecord` | Stores maintenance records. |
| `Vehicle` | `FuelRecord` | Stores fuel records. |
| `VehicleInspection` | `Vehicle` | Refers to the inspected vehicle. |
| `MaintenanceRecord` | `Vehicle` | Refers to the serviced vehicle. |
| `FuelRecord` | `Vehicle` | Refers to the refuelled vehicle. |
| `Trailer` | `Vehicle` | Stores the vehicle to which the trailer is attached. |
| `Cargo` | `CargoPackage` | Contains cargo packages. |
| `Cargo` | `CargoDocument` | Contains supporting documents. |
| `CargoDocument` | `Cargo` | Identifies the cargo described by the document. |
| `OrderItem` | `Cargo` | Refers to the cargo in an order line. |
| `TransportOrder` | `OrderItem` | Contains order items. |
| `TransportOrder` | `Route` | Stores the assigned route. |
| `TransportOrder` | `Trip` | Stores the assigned trip. |
| `Shipment` | `TransportOrder` | Refers to the source order. |
| `Shipment` | `Vehicle` | Stores the vehicle used for loading. |
| `Route` | `RoutePoint` | Contains intermediate route points. |
| `Trip` | `Driver` | Stores the assigned driver. |
| `Trip` | `Vehicle` | Stores the assigned vehicle. |
| `Trip` | `Route` | Stores the route followed by the trip. |
| `Trip` | `TransportOrder` | Contains orders carried on the trip. |
| `Trip` | `Stop` | Contains trip stops. |
| `Schedule` | `Trip` | Stores scheduled trips. |
| `Delivery` | `TransportOrder` | Refers to the order being delivered. |
| `Payment` | `TransportOrder` | Identifies the order being paid for. |
| `Payment` | `Invoice` | Refers to the invoice being settled. |
| `Payment` | `Transaction` | Contains payment and refund transactions. |
| `Invoice` | `TransportOrder` | Refers to the billed order. |
| `Invoice` | `Payment` | Stores payments registered against the invoice. |
| `Transaction` | `Payment` | Refers to the payment associated with the transaction. |
| `Expense` | `Manager` | Stores the manager who approved the expense. |
| `Budget` | `Expense` | Contains expenses assigned to the budget. |
| `SalaryPayment` | `Employee` | Refers to the employee receiving the salary. |
| `FinancialReport` | `Payment` | Collects payments for the reporting period. |
| `FinancialReport` | `Expense` | Collects expenses for the reporting period. |
| `FinancialReport` | `SalaryPayment` | Collects salary payments for the reporting period. |
| `EmployeeRegistry` | `Employee` | Stores registered employees. |
| `CustomerRegistry` | `Customer` | Stores registered customers. |
| `OrderRegistry` | `TransportOrder` | Stores registered orders. |
| `Fleet` | `Vehicle` | Stores vehicles belonging to the fleet. |
| `Fleet` | `Driver` | Stores drivers assigned within the fleet. |
| `Fleet` | `Trip` | Maintains trip history. |
| `Warehouse` | `Cargo` | Stores cargo held in the warehouse. |
| `Department` | `Employee` | Contains department employees. |
| `Department` | `Expense` | Tracks department expenses. |
| `Branch` | `Employee` | Contains branch employees. |
| `Branch` | `Vehicle` | Contains vehicles assigned to the branch. |
| `Branch` | `Warehouse` | Contains branch warehouses. |
| `CompanyPolicy` | `TransportOrder` | Validates an order against company rules. |
| `TransportCompany` | `Branch` | Manages company branches. |
| `TransportCompany` | `Department` | Manages company departments. |
| `TransportCompany` | `Fleet` | Owns the company fleet. |
| `TransportCompany` | `FinancialReport` | Stores company financial reports. |

---

## Custom exceptions

The project defines 12 custom exception classes: one base exception and 11 specialised exceptions.

| Exception | Purpose |
|---|---|
| `TransportCompanyError` | Base exception for domain-specific errors. |
| `InvalidCustomerError` | Invalid customer data or customer operation. |
| `InvalidDriverError` | Invalid driver data or driver operation. |
| `InvalidVehicleError` | Invalid vehicle data or vehicle operation. |
| `VehicleUnavailableError` | A vehicle is not available for the requested operation. |
| `DriverUnavailableError` | A driver is not available for the requested operation. |
| `InvalidCargoError` | Invalid cargo data or cargo operation. |
| `CargoCapacityExceededError` | Cargo exceeds the permitted vehicle capacity. |
| `InvalidRouteError` | Invalid route or route operation. |
| `InvalidOrderStatusError` | An order status transition or order operation is invalid. |
| `PaymentError` | A payment, invoice, or related financial operation fails. |
| `DeliveryError` | A delivery or shipment operation fails. |

---

## Console interface

Run `uv run python main.py` from the repository root to start the interactive console application. The console interface is implemented in `main.py`; domain classes are kept in the `transport_company` package.

The main menu provides these workflows:

1. **Customers** — register individual and corporate customers and display registered customers.
2. **Employees** — add drivers, employees, dispatchers, and managers; display registered employees.
3. **Fleet** — add supported vehicle types and display vehicles in the fleet.
4. **Cargo** — create regular, perishable, fragile, dangerous, and oversized cargo; display cargo records.
5. **Orders** — create orders, add cargo items, approve orders, list orders, and cancel orders.
6. **Routes and trips** — create routes and trips, assign orders to trips, start/finish trips, and display route/trip information.
7. **Finance** — issue invoices, process payments, and display invoices.
8. **Company summary** — display company-level operational counts and totals.

The current application stores objects in memory. Data entered during a run is not persisted after the program exits.

---

## Development setup with `uv`

The project uses [`uv`](https://docs.astral.sh/uv/) to manage the Python environment and dependencies. Development tools are declared in `pyproject.toml`; `uv.lock` records the resolved dependency versions.

### Install `uv`

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Create the environment and install dependencies

Run these commands from the repository root (the directory containing `pyproject.toml`):

```bash
uv python pin 3.14
uv lock
uv sync --group dev
```

The `dev` dependency group should contain the project's development tools, including `pytest`, `coverage`, and `ruff`. The package build configuration uses Hatchling and includes the `transport_company` package.

### Run the console application

```bash
uv run python main.py
```

### Run class unit tests

Tests are located in `tests/`. The suite tests domain classes; the interactive console in `main.py` is intentionally not part of the unit-test scope.

```bash
uv run pytest
```

### Check test coverage

Coverage is measured for the `transport_company` package, not for the console interface:

```bash
uv run coverage erase
uv run coverage run -m pytest -q
uv run coverage report --fail-under=90
```

The coverage command exits with a non-zero status if coverage is below 90%.

### Run Ruff

```bash
uv run ruff check .
```

To apply safe automatic fixes:

```bash
uv run ruff check --fix .
```

### Build distributions

The project is configured with Hatchling as its build backend. To build the Python distributions:

```bash
uv build
```

Build artifacts are written to `dist/` (wheel and source distribution).

---

## Continuous integration

GitHub Actions workflows are stored in `.github/workflows/`.

### `CI.yml`

The CI workflow runs on pushes, pull requests, and manual dispatch. It:

1. Checks out the repository.
2. Installs the configured Python version and `uv`.
3. Installs locked dependencies with `uv sync --locked --group dev`.
4. Runs Ruff (`uv run --locked ruff check .`).
5. Runs the class unit tests with Coverage.
6. Fails if tests fail or total coverage is below 90%.

### `release.yml`

The Release workflow runs when a version tag matching `v*.*.*` is pushed. It repeats the lint, test, and coverage checks, builds distributions with `uv build`, and publishes a GitHub Release with the generated distribution files attached.

To publish a release, update the project version in `pyproject.toml`, commit the changes, and push a version tag. For example:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

A release is not published if linting, tests, coverage enforcement, or package building fails.

---

## Project structure

```text
Laboratory-2/
├── .github/
│   └── workflows/
│       ├── CI.yml                 # Lint, class tests, and coverage gate
│       └── release.yml            # Build and publish GitHub Releases
├── tests/
│   └── test.py                    # Unit tests for domain classes
├── transport_company/
│   ├── __init__.py                # Public package exports
│   ├── people.py                  # Customers and employees
│   ├── vehicles.py                # Vehicles and vehicle records
│   ├── cargo.py                   # Cargo, packages, and cargo documents
│   ├── transport.py               # Orders, routes, shipments, trips, deliveries
│   ├── finance.py                 # Payments, invoices, expenses, budgets, reports
│   ├── company.py                 # Registries, fleet, branches, warehouse, policies
│   └── exceptions.py              # Custom domain exceptions
├── .coveragerc                    # Coverage source and reporting configuration
├── .python-version                # Local Python version selected by uv
├── uv.lock                        # Locked dependency versions
├── pyproject.toml                 # Project, build, pytest, and Ruff configuration
├── main.py                        # Interactive console interface
└── README.md                      # Project documentation
```

---

## Notes

- The project requires Python 3.10 or newer; the documented local and CI setup uses Python 3.14.
- `transport_company/__init__.py` exports the public classes and custom exceptions, allowing imports from the package root, for example `from transport_company import TransportCompany, Driver, Truck`.
- Modules inside `transport_company` should use relative imports between package modules (for example, `from .exceptions import InvalidCargoError`).
- Unit tests cover domain classes only. The console interface is not included in the test suite.
- The application currently uses in-memory data structures and does not persist records between runs.
- The CI coverage threshold is 90%. A coverage percentage measures executed code and does not prove that every business scenario is fully tested.
- Keep this README aligned with the actual class implementations, CLI menu, package configuration, and GitHub Actions workflows as the project evolves.
