# Library Management System — Python OOP Project

An object-oriented project that models the core operations of a library. It includes reader and staff management, a library catalogue, physical and digital items, circulation, loans and returns, reservations and waiting lists, fines and payments, purchasing, library facilities, events, and operational reports.

The project is organised as a Python package (`library_system`) with a separate console interface (`cli`) and `main.py` as the entry point. It uses in-memory objects and collections; no database or external service is required.

---

## Features

- Register readers, student readers, child readers, and library staff.
- Manage library cards, memberships, and reading lists.
- Maintain a catalogue of books, magazines, audiobooks, theses, and e-books.
- Manage authors, publishers, categories, item copies, and reviews.
- Search and browse the catalogue and track item-copy availability.
- Issue and return items, renew loans, and maintain return records.
- Place reservations and manage waiting lists and interlibrary requests.
- Enforce lending rules, age restrictions, loan limits, overdue rules, and reader status.
- Register lost items and handle related library operations.
- Calculate fines, accept payments, and manage donations.
- Manage suppliers, purchase orders, purchase lines, and budgets.
- Manage branches, shelves, reading rooms, seat bookings, library events, and event registrations.
- Maintain opening hours, staff shifts, and inventory audits.
- Generate library and reader-related reports.
- Load demonstration data through the console menu.

---

## Classes by package

The domain model contains **57 classes** distributed across the library-system package, plus **19 custom exception classes**.

### `library_system.people` — Readers and staff

| Class | Main responsibility |
|---|---|
| `Person` | Common personal information and contact details. |
| `Reader` | Library reader profile and reader-related operations. |
| `StudentReader` | Reader specialization for students. |
| `ChildReader` | Reader specialization for children and age-related rules. |
| `Staff` | Base class for library employees. |
| `Librarian` | Reader-facing library and circulation operations. |
| `Cataloger` | Catalogue maintenance and item metadata. |
| `Director` | Library management and approval responsibilities. |
| `Membership` | Reader membership and membership status. |
| `LibraryCard` | Reader card, validity, and lending identification. |
| `ReadingList` | A reader's saved list of library items. |

### `library_system.catalog` — Catalogue and library items

| Class | Main responsibility |
|---|---|
| `LibraryItem` | Base representation of a catalogue item. |
| `Book` | Printed book metadata. |
| `Magazine` | Magazine and periodical metadata. |
| `AudioBook` | Audiobook metadata. |
| `Thesis` | Academic thesis metadata. |
| `EBook` | Electronic book metadata. |
| `ItemCopy` | A physical or lendable copy and its availability. |
| `Author` | Author information and associated works. |
| `Publisher` | Publisher information and published items. |
| `Category` | Catalogue classification. |
| `Review` | Reader review and rating. |
| `Catalog` | Collection and catalogue search/management. |

### `library_system.circulation` — Loans and reader services

| Class | Main responsibility |
|---|---|
| `Loan` | A lending record, due date, and loan status. |
| `LoanDesk` | Coordinates issuing and returning items. |
| `LoanPolicy` | Lending limits and circulation rules. |
| `Renewal` | A loan renewal request or record. |
| `ReturnRecord` | Information about an item return. |
| `Reservation` | A reader's reservation for an item. |
| `WaitingList` | Queue of readers waiting for an item. |
| `InterlibraryRequest` | Request for an item from another library. |
| `LostItemReport` | Record of a lost library item. |
| `Subscription` | Reader subscription-related information. |
| `Notification` | Reader notification records. |

### `library_system.finance` — Fines, payments, and purchasing

| Class | Main responsibility |
|---|---|
| `Fine` | Fine amount and payment status. |
| `FinePolicy` | Rules used to calculate fines. |
| `Payment` | Payment record and payment processing. |
| `Donation` | Library donation record. |
| `Budget` | Budget limits and spending tracking. |
| `Supplier` | Supplier information. |
| `PurchaseOrder` | Purchase order lifecycle and approval. |
| `PurchaseLine` | Individual item/quantity/price line in a purchase. |

### `library_system.facilities` — Library buildings and activities

| Class | Main responsibility |
|---|---|
| `Branch` | Library branch and its resources. |
| `Shelf` | Shelf and item placement. |
| `ReadingRoom` | Reading-room information and capacity. |
| `SeatBooking` | Booking a seat in a reading room. |
| `LibraryEvent` | Library event details and registration. |
| `EventRegistration` | Reader registration for an event. |
| `InventoryAudit` | Inventory inspection and audit records. |
| `StaffShift` | Staff shift information. |
| `OpeningHours` | Branch opening hours. |

### `library_system.services` — Application services and registries

| Class | Main responsibility |
|---|---|
| `Library` | Main library facade coordinating domain operations. |
| `ReaderServices` | Reader-oriented application workflows. |
| `ReaderRegistry` | Registration, lookup, and management of readers. |
| `StaffRegistry` | Registration, lookup, and management of staff. |
| `LibraryReport` | Library-level summaries and reports. |

### Supporting modules

- `library_system.exceptions` — 19 domain-specific exceptions derived from `LibraryError`.
- `library_system.constants` — Shared numeric values, fees, limits, and rule text.
- `library_system.enums` — Enumerations for statuses and domain types.
- `library_system.ids` — Generation and handling of domain identifiers.
- `library_system.timeutils` — Date and time helper functions.
- `library_system.validation` — Shared validation utilities.

---

## Associations

An association is a relationship where an object stores a reference to another object, contains it in a collection, or receives it as a method parameter. The domain model contains more than 30 such relationships. Examples include:

| From | To | Relationship |
|---|---|---|
| `Reader` | `LibraryCard` | A reader is associated with a library card. |
| `Reader` | `Membership` | A reader has membership information. |
| `Reader` | `Loan` | A reader has loan records. |
| `Reader` | `ReadingList` | A reader maintains a reading list. |
| `LibraryCard` | `Reader` | The card identifies its reader. |
| `LibraryItem` | `Author` | Catalogue item metadata references authors. |
| `LibraryItem` | `Publisher` | Catalogue item metadata references a publisher. |
| `LibraryItem` | `Category` | Catalogue items are classified by category. |
| `ItemCopy` | `LibraryItem` | A copy belongs to a catalogue item. |
| `Catalog` | `LibraryItem` | The catalogue stores and searches items. |
| `Loan` | `Reader` | A loan identifies the borrowing reader. |
| `Loan` | `ItemCopy` | A loan identifies the copy being borrowed. |
| `LoanDesk` | `LoanPolicy` | The desk applies circulation rules. |
| `Loan` | `Renewal` | A loan may have renewal records. |
| `ReturnRecord` | `Loan` | A return record refers to a loan. |
| `Reservation` | `Reader` | A reservation identifies the requesting reader. |
| `Reservation` | `LibraryItem` | A reservation identifies the requested item. |
| `WaitingList` | `Reservation` | The waiting list manages queued reservations. |
| `InterlibraryRequest` | `Reader` | A request identifies its reader. |
| `Fine` | `Loan` | A fine may be associated with an overdue loan. |
| `Payment` | `Fine` | A payment can settle a fine. |
| `PurchaseOrder` | `Supplier` | A purchase order identifies its supplier. |
| `PurchaseOrder` | `PurchaseLine` | A purchase order contains purchase lines. |
| `PurchaseOrder` | `Budget` | Purchase approval uses a budget. |
| `Branch` | `Shelf` | A branch contains shelves. |
| `Branch` | `ReadingRoom` | A branch contains reading rooms. |
| `ReadingRoom` | `SeatBooking` | A reading room has seat bookings. |
| `LibraryEvent` | `EventRegistration` | An event contains registrations. |
| `EventRegistration` | `Reader` | A registration identifies its reader. |
| `InventoryAudit` | `Branch` | An audit is associated with a branch. |
| `StaffShift` | `Staff` | A shift identifies a staff member. |
| `Library` | `Catalog` | The library coordinates catalogue operations. |
| `Library` | `ReaderRegistry` | The library manages registered readers. |
| `Library` | `StaffRegistry` | The library manages registered staff. |
| `Library` | `LibraryReport` | The library provides operational reporting. |

---

## Custom exceptions

The project defines **19 custom exception classes**: one base exception and 18 specialised exceptions.

| Exception | Purpose |
|---|---|
| `LibraryError` | Base exception for library-domain errors. |
| `ActiveLoansError` | An operation is blocked by active loans. |
| `AgeRestrictionError` | A reader does not meet an item's age requirement. |
| `BudgetExceededError` | An operation exceeds the available budget. |
| `CapacityExceededError` | A capacity limit has been exceeded. |
| `CardExpiredError` | A library card is expired. |
| `InvalidStatusTransitionError` | A status change is not allowed. |
| `ItemNotAvailableError` | An item or copy is unavailable. |
| `ItemNotFoundError` | A requested catalogue item or copy cannot be found. |
| `LoanLimitExceededError` | The reader has reached the lending limit. |
| `OverdueLoansError` | Overdue loans prevent an operation. |
| `PaymentError` | A payment operation fails. |
| `ReaderBlockedError` | A blocked reader cannot perform the operation. |
| `ReaderNotFoundError` | A reader cannot be found. |
| `RenewalNotAllowedError` | A loan cannot be renewed. |
| `ReservationError` | A reservation operation fails. |
| `StaffNotFoundError` | A staff member cannot be found. |
| `UnpaidFineError` | An unpaid fine prevents an operation. |
| `ValidationError` | Domain data fails validation. |

---

## Console interface

Run `python main.py` from the `Lab3` directory to start the interactive console application. The entry point calls `cli.app.run`; the console code is kept in the `cli` package, while domain classes are kept in `library_system`.

The console is divided into workflows for:

1. Readers and library cards.
2. Staff management.
3. Catalogue and item copies.
4. Circulation: loans, returns, renewals, reservations, and waiting lists.
5. Facilities: branches, rooms, seat bookings, and events.
6. Finance: fines, payments, budgets, and purchasing.
7. Reports and library summaries.
8. Loading demonstration data.

The **«Загрузить демонстрационные данные»** menu option creates sample library data, including a branch, staff, readers, books, and copies. Generated identifiers are displayed in the relevant lists.

The application currently stores objects in memory. Data entered during a run is not persisted after the program exits.

---

## Development setup

The project supports Python 3.10 or newer. The project configuration uses `uv` and Hatchling; the development dependencies are `pytest`, `coverage`, and `ruff`. There are no runtime dependencies.

### Install dependencies with `uv`

Run these commands from the `Lab3` directory:

```bash
uv sync
```

### Or install with `pip`

```bash
python -m pip install -r requirements.txt
```

### Run the console application

```bash
python main.py
```

### Run unit tests

Tests are located in `tests/`.

```bash
python -m pytest
```

### Measure test coverage

Coverage is configured for the `library_system` and `cli` packages and uses branch coverage.

```bash
python -m coverage run -m pytest
python -m coverage report
```

### Run Ruff

```bash
ruff check .
ruff format --check .
```

### Build distributions

The project uses Hatchling as its build backend.

```bash
uv build
```

---

## Continuous integration

The GitHub Actions workflow is stored at `.github/workflows/Lab3-CI.yml`.

It runs on pushes to `main` and `lab3`, and on pull requests. The workflow:

1. Checks out the repository.
2. Sets up `uv` and Python.
3. Installs dependencies with `uv sync --frozen`.
4. Runs Ruff lint checks.
5. Checks formatting with `ruff format --check`.
6. Runs tests with coverage.
7. Fails if coverage is below **91%**.

The CI matrix currently uses Python 3.10 and 3.12.

---

## Project structure

```text
Lab3/
├── cli/
│   ├── app.py                  # Console application entry point
│   ├── menu.py                 # Menu navigation
│   ├── context.py              # Shared CLI context
│   ├── console_io.py           # Console input and output
│   ├── demo_data.py            # Demonstration data
│   ├── texts.py                # Interface text
│   ├── formatters.py           # Output formatting
│   └── *_screen.py             # Screens for domain workflows
├── library_system/
│   ├── people/                 # Readers, staff, cards, memberships
│   ├── catalog/                # Items, copies, authors, catalogue
│   ├── circulation/             # Loans, returns, reservations
│   ├── finance/                 # Fines, payments, budgets, purchases
│   ├── facilities/              # Branches, rooms, events, bookings
│   ├── services/                # Library facade, registries, reports
│   ├── exceptions/              # Custom domain exceptions
│   ├── constants.py             # Shared constants
│   ├── enums.py                 # Domain enumerations
│   ├── ids.py                   # Identifier utilities
│   ├── timeutils.py             # Date/time helpers
│   └── validation.py             # Validation utilities
├── people/                      # Additional C++ people-related files
├── tests/
│   ├── factories.py              # Test object factories
│   ├── conftest.py               # Pytest fixtures
│   └── test_*.py                 # Unit and CLI tests
├── main.py                       # Application entry point
├── pyproject.toml                # Project, build, pytest, coverage, Ruff config
├── requirements.txt               # Pip requirements
├── uv.lock                       # Locked dependency versions
└── README.md                     # Project documentation
```

---

## Notes

- Python 3.10+ is required.
- The package is named `library_system`.
- The console interface is implemented in the separate `cli` package.
- Runtime dependencies are empty; development tools are installed separately.
- The application uses in-memory data structures and does not persist records between runs.
- Coverage includes both `library_system` and `cli`; CI enforces a 91% threshold.
- The current repository tree does not include `tools/check_metrics.py`, although the existing Lab3 README mentions it; the metrics table in that README should therefore be treated as documented project figures, not a result reproducible from that script in the current checkout.\n- Keep this README aligned with the actual class implementations, console menu, package configuration, and GitHub Actions workflow as the project evolves.
