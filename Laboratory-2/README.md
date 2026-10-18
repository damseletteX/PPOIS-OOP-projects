# Transportation Company — OOP Project

A Python 3 domain model and demonstration program for a **transportation company**:
customers, employees, transport orders, shipments, fleet management, route planning,
delivery tracking, warehouse operations, payments, invoicing, and insurance.

The project includes a console interface, application services, domain entities,
custom exceptions, and unit tests. It is designed to be installed, built, and tested
from the command line without relying on a particular IDE.

---

## Classes by package

### `people` — Customers and employees

| Class | Fields | Key methods |
|---|---|---|
| `Person` | `name`, `email`, `phone`, `address`, `related_entity_id`, `notes` | `update_contact_details()`, `verify_identity()` |
| `Customer` | `customer_code`, `billing_address`, `preferred_contact`, `credit_limit`, `related_entity_id`, `notes` | `place_order()`, `request_delivery_quote()` |
| `BusinessCustomer` | `company_name`, `tax_number`, `contract_number`, `payment_terms_days`, `related_entity_id`, `notes` | `approve_contract_terms()`, `request_monthly_statement()` |
| `PrivateCustomer` | `identity_document`, `delivery_instructions`, `notification_opt_in`, `customer_since`, `related_entity_id`, `notes` | `confirm_delivery_address()`, `change_notification_preferences()` |
| `Employee` | `employee_number`, `hire_date`, `salary`, `employment_status`, `related_entity_id`, `notes` | `request_leave()`, `record_performance_review()` |
| `Driver` | `license_number`, `license_category`, `license_expiry`, `hours_driven_today`, `related_entity_id`, `notes` | `accept_assignment()`, `record_driver_inspection()`, `report_fatigue()` |
| `Dispatcher` | `dispatch_area`, `shift_start`, `shift_end`, `active_assignments`, `related_entity_id`, `notes` | `assign_vehicle_to_trip()`, `reassign_trip()`, `resolve_dispatch_conflict()` |
| `Mechanic` | `specialization`, `certification_code`, `workshop_id`, `open_work_orders`, `related_entity_id`, `notes` | `diagnose_vehicle_fault()`, `complete_repair_job()` |
| `Manager` | `department`, `approval_limit`, `management_level`, `reports_to`, `related_entity_id`, `notes` | `approve_expense()`, `review_operational_metrics()` |
| `WarehouseWorker` | `warehouse_id`, `safety_training_date`, `forklift_certified`, `assigned_zone`, `related_entity_id`, `notes` | `record_loading_activity()`, `confirm_cargo_staging()` |

### `orders` — Orders, shipments and cargo

| Class | Fields | Key methods |
|---|---|---|
| `TransportOrder` | `order_number`, `created_at`, `status`, `priority`, `customer_id`, `related_order_id` | `validate_order()`, `cancel_order()`, `change_delivery_window()` |
| `Shipment` | `shipment_number`, `weight_kg`, `volume_m3`, `declared_value`, `customer_id`, `related_order_id` | `split_shipment()`, `consolidate_with_shipment()` |
| `CargoItem` | `item_code`, `description`, `quantity`, `handling_code`, `customer_id`, `related_order_id` | `mark_as_fragile()`, `calculate_chargeable_weight()` |
| `Package` | `package_id`, `length_cm`, `width_cm`, `height_cm`, `customer_id`, `related_order_id` | `calculate_volume()`, `assign_package_label()` |
| `Pallet` | `pallet_code`, `pallet_type`, `max_load_kg`, `is_returnable`, `customer_id`, `related_order_id` | `check_load_capacity()`, `register_pallet_return()` |
| `DangerousGoodsDeclaration` | `un_number`, `hazard_class`, `packing_group`, `emergency_contact`, `customer_id`, `related_order_id` | `validate_hazard_documentation()`, `prepare_transport_declaration()` |
| `TemperatureRequirement` | `minimum_celsius`, `maximum_celsius`, `monitoring_interval_minutes`, `excursion_policy`, `customer_id`, `related_order_id` | `check_temperature_reading()`, `record_temperature_excursion()` |
| `DeliveryProof` | `proof_number`, `signed_by`, `delivered_at`, `photo_reference`, `customer_id`, `related_order_id` | `verify_recipient_signature()`, `attach_delivery_evidence()` |
| `ReturnRequest` | `return_number`, `reason`, `requested_at`, `return_status`, `customer_id`, `related_order_id` | `approve_return()`, `schedule_return_collection()` |
| `OrderLine` | `line_number`, `item_description`, `quantity`, `unit_price`, `customer_id`, `related_order_id` | `calculate_line_total()`, `change_quantity()` |

### `fleet` — Vehicles and maintenance

| Class | Fields | Key methods |
|---|---|---|
| `Vehicle` | `registration_number`, `make`, `model`, `capacity_kg`, `vehicle_id`, `assigned_employee_id` | `check_capacity_for_shipment()`, `mark_out_of_service()`, `record_odometer_reading()` |
| `Truck` | `trailer_type`, `axle_count`, `fuel_type`, `emissions_class`, `vehicle_id`, `assigned_employee_id` | `attach_trailer()`, `check_height_restriction()` |
| `Van` | `cargo_volume_m3`, `urban_access_permit`, `rear_door_height_cm`, `has_refrigeration`, `vehicle_id`, `assigned_employee_id` | `check_urban_access()`, `optimise_parcel_loading()` |
| `Trailer` | `trailer_number`, `max_payload_kg`, `trailer_length_m`, `inspection_due`, `vehicle_id`, `assigned_employee_id` | `couple_to_vehicle()`, `schedule_trailer_inspection()` |
| `RefrigeratedUnit` | `target_temperature`, `current_temperature`, `unit_serial`, `last_calibration`, `vehicle_id`, `assigned_employee_id` | `set_target_temperature()`, `raise_temperature_alarm()` |
| `VehicleInspection` | `inspection_id`, `inspection_date`, `inspector_name`, `result`, `vehicle_id`, `assigned_employee_id` | `record_defect()`, `certify_roadworthiness()` |
| `MaintenanceRecord` | `record_id`, `maintenance_type`, `performed_at`, `cost`, `vehicle_id`, `assigned_employee_id` | `close_maintenance_record()`, `calculate_next_service_date()` |
| `FuelTransaction` | `transaction_id`, `litres`, `price_per_litre`, `station_name`, `vehicle_id`, `assigned_employee_id` | `calculate_fuel_cost()`, `flag_unusual_consumption()` |
| `Tyre` | `tyre_serial`, `position`, `tread_depth_mm`, `installed_at`, `vehicle_id`, `assigned_employee_id` | `check_tread_compliance()`, `record_tyre_rotation()` |
| `VehicleDocument` | `document_number`, `document_type`, `valid_until`, `issuing_authority`, `vehicle_id`, `assigned_employee_id` | `check_document_validity()`, `request_document_renewal()` |

### `routing` — Routes and trips

| Class | Fields | Key methods |
|---|---|---|
| `Route` | `route_code`, `origin`, `destination`, `distance_km`, `trip_id`, `related_route_id` | `calculate_estimated_duration()`, `avoid_restricted_roads()`, `recalculate_route()` |
| `RouteStop` | `stop_number`, `location`, `planned_arrival`, `stop_type`, `trip_id`, `related_route_id` | `reschedule_stop()`, `confirm_stop_completion()` |
| `Trip` | `trip_number`, `departure_time`, `arrival_deadline`, `trip_status`, `trip_id`, `related_route_id` | `start_trip()`, `complete_trip()`, `report_delay()` |
| `TripAssignment` | `assignment_id`, `assigned_at`, `assignment_status`, `dispatcher_id`, `trip_id`, `related_route_id` | `confirm_assignment()`, `withdraw_assignment()` |
| `TollCharge` | `toll_id`, `road_name`, `charge_amount`, `charged_at`, `trip_id`, `related_route_id` | `allocate_toll_to_trip()`, `dispute_toll_charge()` |
| `FuelStop` | `stop_id`, `fuel_station`, `planned_litres`, `planned_time`, `trip_id`, `related_route_id` | `confirm_fuel_stop()`, `compare_fuel_prices()` |
| `Geofence` | `geofence_id`, `center_latitude`, `center_longitude`, `radius_meters`, `trip_id`, `related_route_id` | `check_vehicle_entry()`, `trigger_geofence_event()` |
| `TrafficIncident` | `incident_id`, `incident_type`, `reported_at`, `severity`, `trip_id`, `related_route_id` | `estimate_delay_impact()`, `propose_route_detour()` |
| `DeliveryWindow` | `window_id`, `start_time`, `end_time`, `strictness`, `trip_id`, `related_route_id` | `check_window_feasibility()`, `negotiate_new_window()` |
| `TrackingEvent` | `event_id`, `event_type`, `occurred_at`, `latitude`, `trip_id`, `related_route_id` | `record_location_update()`, `notify_customer_of_milestone()` |

### `finance` — Finance and insurance

| Class | Fields | Key methods |
|---|---|---|
| `Invoice` | `invoice_number`, `issued_at`, `due_date`, `total_amount`, `customer_id`, `related_document_id` | `calculate_amount_due()`, `mark_as_paid()`, `issue_credit_note()` |
| `Payment` | `payment_reference`, `amount`, `payment_method`, `received_at`, `customer_id`, `related_document_id` | `allocate_payment_to_invoice()`, `refund_payment()` |
| `RateCard` | `rate_card_code`, `base_rate`, `per_km_rate`, `effective_from`, `customer_id`, `related_document_id` | `quote_transport_price()`, `apply_surcharge()` |
| `Discount` | `discount_code`, `percentage`, `valid_from`, `valid_until`, `customer_id`, `related_document_id` | `check_discount_eligibility()`, `apply_discount()` |
| `Expense` | `expense_id`, `category`, `amount`, `incurred_at`, `customer_id`, `related_document_id` | `submit_for_approval()`, `allocate_expense_to_trip()` |
| `PayrollRecord` | `payroll_id`, `period_start`, `period_end`, `gross_pay`, `customer_id`, `related_document_id` | `calculate_net_pay()`, `finalise_payroll()` |
| `FuelBudget` | `budget_id`, `period`, `allocated_amount`, `spent_amount`, `customer_id`, `related_document_id` | `calculate_budget_variance()`, `forecast_fuel_spend()` |
| `InsurancePolicy` | `policy_number`, `provider`, `coverage_limit`, `expires_at`, `customer_id`, `related_document_id` | `check_claim_coverage()`, `renew_policy()` |
| `Claim` | `claim_number`, `claim_type`, `claim_amount`, `claim_status`, `customer_id`, `related_document_id` | `submit_claim_evidence()`, `settle_claim()` |
| `FinancialReport` | `report_id`, `period`, `revenue`, `operating_cost`, `customer_id`, `related_document_id` | `calculate_profit_margin()`, `export_financial_summary()` |

### `operations` — Warehouse and operations

| Class | Fields | Key methods |
|---|---|---|
| `Warehouse` | `warehouse_code`, `address`, `capacity_pallets`, `operating_hours`, `warehouse_id`, `related_entity_id` | `check_storage_capacity()`, `allocate_storage_zone()` |
| `StorageZone` | `zone_code`, `zone_type`, `capacity`, `temperature_controlled`, `warehouse_id`, `related_entity_id` | `reserve_storage_space()`, `audit_zone_occupancy()` |
| `LoadingPlan` | `plan_id`, `loading_date`, `sequence_rule`, `prepared_by`, `warehouse_id`, `related_entity_id` | `optimise_loading_sequence()`, `validate_weight_distribution()` |
| `Manifest` | `manifest_number`, `created_at`, `trip_number`, `seal_number`, `warehouse_id`, `related_entity_id` | `add_shipment_to_manifest()`, `reconcile_manifest()` |
| `CustomsDeclaration` | `declaration_number`, `destination_country`, `commodity_code`, `customs_value`, `warehouse_id`, `related_entity_id` | `validate_customs_fields()`, `submit_customs_declaration()` |
| `Permit` | `permit_number`, `permit_type`, `valid_from`, `valid_until`, `warehouse_id`, `related_entity_id` | `check_permit_for_route()`, `request_permit_extension()` |
| `ServiceLevelAgreement` | `agreement_number`, `max_delivery_hours`, `on_time_target_percent`, `penalty_rate`, `warehouse_id`, `related_entity_id` | `check_sla_compliance()`, `calculate_service_credit()` |
| `IncidentReport` | `incident_number`, `incident_category`, `description`, `reported_by`, `warehouse_id`, `related_entity_id` | `classify_incident()`, `escalate_incident()` |
| `Notification` | `notification_id`, `channel`, `recipient`, `message`, `warehouse_id`, `related_entity_id` | `send_notification()`, `schedule_reminder()` |
| `AuditLogEntry` | `entry_id`, `actor_id`, `action`, `timestamp`, `warehouse_id`, `related_entity_id` | `record_audit_event()`, `search_related_events()` |

---

## Associations

An association is a relationship in which one class references another as a field
or uses it as a method parameter. The domain model documents the following
**50 relationships**:

| From | To | Description |
|---|---|---|
| `Customer` | `TransportOrder` | places |
| `BusinessCustomer` | `Invoice` | is billed through |
| `PrivateCustomer` | `DeliveryProof` | receives |
| `TransportOrder` | `Shipment` | contains |
| `TransportOrder` | `Customer` | belongs to |
| `TransportOrder` | `DeliveryWindow` | specifies |
| `Shipment` | `CargoItem` | contains |
| `CargoItem` | `Package` | is packed in |
| `Package` | `Pallet` | may be loaded on |
| `Shipment` | `DangerousGoodsDeclaration` | may require |
| `Shipment` | `TemperatureRequirement` | may specify |
| `Shipment` | `DeliveryProof` | is confirmed by |
| `ReturnRequest` | `TransportOrder` | refers to |
| `OrderLine` | `TransportOrder` | belongs to |
| `Driver` | `TripAssignment` | receives |
| `Dispatcher` | `TripAssignment` | creates |
| `TripAssignment` | `Trip` | assigns resources to |
| `Trip` | `Route` | follows |
| `Route` | `RouteStop` | contains |
| `Trip` | `Vehicle` | uses |
| `Truck` | `Trailer` | may tow |
| `Vehicle` | `VehicleInspection` | undergoes |
| `Vehicle` | `MaintenanceRecord` | has |
| `Vehicle` | `FuelTransaction` | records |
| `Vehicle` | `Tyre` | uses |
| `Vehicle` | `VehicleDocument` | requires |
| `RefrigeratedUnit` | `TemperatureRequirement` | fulfils |
| `Trip` | `TollCharge` | incurs |
| `Trip` | `FuelStop` | may include |
| `Route` | `Geofence` | may cross |
| `Route` | `TrafficIncident` | is affected by |
| `Trip` | `TrackingEvent` | generates |
| `Trip` | `DeliveryWindow` | must meet |
| `Invoice` | `Payment` | is settled by |
| `Invoice` | `RateCard` | is priced using |
| `RateCard` | `Discount` | may apply |
| `Expense` | `Trip` | is allocated to |
| `Employee` | `PayrollRecord` | has |
| `FuelBudget` | `FuelTransaction` | covers |
| `InsurancePolicy` | `Claim` | covers |
| `Warehouse` | `StorageZone` | contains |
| `WarehouseWorker` | `Warehouse` | works at |
| `LoadingPlan` | `Manifest` | supports |
| `Manifest` | `Shipment` | lists |
| `CustomsDeclaration` | `Shipment` | declares |
| `Permit` | `Route` | authorises |
| `ServiceLevelAgreement` | `Customer` | governs |
| `IncidentReport` | `Trip` | may concern |
| `Notification` | `Customer` | is sent to |
| `AuditLogEntry` | `Employee` | records activity of |

---

## Custom exceptions

Domain-specific exceptions represent invalid operations and business-rule violations.
The project defines:

| Exception | Purpose |
|---|---|
| `TransportCompanyError` | Base class for domain errors. |
| `InvalidOrderError` | An order or shipment fails validation. |
| `CustomerNotFoundError` | A requested customer or employee record cannot be found. |
| `VehicleUnavailableError` | A vehicle cannot be assigned. |
| `DriverUnavailableError` | A driver cannot be assigned. |
| `CapacityExceededError` | Cargo exceeds vehicle or storage capacity. |
| `RouteNotFeasibleError` | A route is unsafe or not legally feasible. |
| `DeliveryWindowError` | A delivery cannot meet its delivery window. |
| `PaymentProcessingError` | A payment operation fails. |
| `InvoiceStateError` | An invoice state transition is invalid. |
| `MaintenanceRequiredError` | A vehicle requires maintenance before use. |
| `PermitExpiredError` | A required permit has expired. |
| `DangerousGoodsComplianceError` | Dangerous-goods requirements are not met. |
| `TemperatureExcursionError` | Cargo temperature is outside its permitted range. |
| `DuplicateReferenceError` | A unique business reference already exists. |
| `ResourceConflictError` | A resource is double-booked or otherwise conflicts. |

---

## CLI scenarios

Run `python main.py` to open the interactive console menu. The CLI is kept separate
from the application service layer in `transport_company/application.py`.

The menu currently demonstrates these workflows:

1. **Add an employee** — validate and store an employee record.
2. **Remove an employee** — remove an existing employee by ID.
3. **Register a shipment** — validate the reference, destination, and positive weight.
4. **Dispatch a shipment** — change a registered shipment to `in_transit`.
5. **Generate a report** — show employee count, shipment count, shipments in transit, and total weight.

---

## Tests, coverage, and command-line setup

The project uses `pytest` and `pytest-cov`. Tests can be run from a terminal and do not
require an IDE. The pytest configuration sets a minimum coverage threshold of 91%.
A passing test run means the configured coverage threshold was met; it does not by itself
prove that every domain method implements complete production business logic.

### Install

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e . -r requirements.txt
```

### Run the application

```bash
python main.py
```

### Run unit tests and check coverage

```bash
python -m pytest
```

### Optional Makefile commands

```bash
make install
make run
make test
```

---

## Project structure

```text
main.py                         # Console menu (CLI)
pyproject.toml                  # Build and pytest configuration
requirements.txt                # Test dependencies
Makefile                        # Optional command shortcuts
transport_company/
  application.py                # Application/service layer used by the CLI
  people.py                     # Customers and employees
  orders.py                     # Orders, shipments and cargo
  fleet.py                      # Vehicles and maintenance
  routing.py                    # Routes, trips and tracking
  finance.py                    # Invoices, payments and insurance
  operations.py                 # Warehouse and operational records
  associations.py               # Explicit association catalogue
  exceptions.py                 # Custom domain exceptions
tests/
  test_application.py            # Application workflow tests
  test_domain_catalog.py          # Domain constructors and method smoke tests
BEHAVIOR_CATALOG.md              # Expanded domain behavior catalogue
```

## Notes

- Python 3.14 or newer is specified in `pyproject.toml`.
- The CLI and application service layer are separate from the domain entity modules.
- The current domain catalogue includes methods whose implementations are still basic placeholders;
  extend them with concrete validation, calculations, state changes, and focused tests before production use.
- Keep the README synchronized with the implementation as the domain model evolves.
