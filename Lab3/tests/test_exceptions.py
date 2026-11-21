import pytest

from library_system import (
    ActiveLoansError,
    AgeRestrictionError,
    BudgetExceededError,
    CapacityExceededError,
    CardExpiredError,
    InvalidStatusTransitionError,
    ItemNotAvailableError,
    ItemNotFoundError,
    LibraryError,
    LoanLimitExceededError,
    OverdueLoansError,
    PaymentError,
    ReaderBlockedError,
    ReaderNotFoundError,
    RenewalNotAllowedError,
    ReservationError,
    StaffNotFoundError,
    UnpaidFineError,
    ValidationError,
)

CASES = [
    (ValidationError("Имя", "пусто"), "Имя"),
    (ItemNotFoundError("IT-1"), "IT-1"),
    (ReaderNotFoundError("RD-1"), "RD-1"),
    (StaffNotFoundError("ST-1"), "ST-1"),
    (ItemNotAvailableError("Книга"), "Книга"),
    (LoanLimitExceededError("Иван", 5), "5"),
    (ReaderBlockedError("Иван", "причина"), "причина"),
    (CardExpiredError("CD-1", "2026-01-01"), "2026-01-01"),
    (RenewalNotAllowedError("лимит"), "лимит"),
    (UnpaidFineError("Иван", 12.5), "12.50"),
    (OverdueLoansError("Иван", 2), "2"),
    (ActiveLoansError("Иван", 3), "3"),
    (ReservationError("очередь"), "очередь"),
    (PaymentError("переплата"), "переплата"),
    (BudgetExceededError(100.0, 50.0), "50.00"),
    (CapacityExceededError("Зал", 20), "20"),
    (AgeRestrictionError("Книга", 16), "16"),
    (InvalidStatusTransitionError("Выдача", "a", "b"), "Выдача"),
]


@pytest.mark.parametrize("error, expected_fragment", CASES)
def test_message_contains_details(error, expected_fragment):
    assert expected_fragment in str(error)


@pytest.mark.parametrize("error, expected_fragment", CASES)
def test_all_errors_share_base_class(error, expected_fragment):
    assert isinstance(error, LibraryError)
