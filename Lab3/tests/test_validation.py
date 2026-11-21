import pytest

from library_system import InvalidStatusTransitionError, LoanStatus, ValidationError
from library_system.validation import (
    ensure_transition,
    is_valid_isbn,
    require_email,
    require_in_range,
    require_isbn,
    require_non_negative,
    require_positive,
    require_text,
)

from .factories import VALID_ISBN


def test_require_text_strips_spaces():
    assert require_text("  Иван ", "Имя") == "Иван"


def test_require_text_rejects_blank():
    with pytest.raises(ValidationError):
        require_text("   ", "Имя")


def test_require_positive_accepts_and_rejects():
    assert require_positive(3, "Число") == 3
    with pytest.raises(ValidationError):
        require_positive(0, "Число")


def test_require_non_negative_accepts_zero():
    assert require_non_negative(0, "Число") == 0
    with pytest.raises(ValidationError):
        require_non_negative(-1, "Число")


def test_require_in_range_bounds():
    assert require_in_range(5, 1, 5, "Оценка") == 5
    with pytest.raises(ValidationError):
        require_in_range(6, 1, 5, "Оценка")


def test_require_email_allows_empty_and_rejects_without_at():
    assert require_email("", "Email") == ""
    assert require_email(" a@b.by ", "Email") == "a@b.by"
    with pytest.raises(ValidationError):
        require_email("abc", "Email")


def test_isbn_checksum():
    assert is_valid_isbn(VALID_ISBN)
    assert not is_valid_isbn("9780132350885")
    assert not is_valid_isbn("12345")
    assert not is_valid_isbn("97801323508ab")


def test_require_isbn_removes_hyphens():
    assert require_isbn("978-0-13-235088-4", "ISBN") == VALID_ISBN
    with pytest.raises(ValidationError):
        require_isbn("978-0-13-235088-5", "ISBN")


def test_ensure_transition():
    ensure_transition("Выдача", LoanStatus.ACTIVE, {LoanStatus.ACTIVE}, LoanStatus.RETURNED)
    with pytest.raises(InvalidStatusTransitionError):
        ensure_transition("Выдача", LoanStatus.LOST, {LoanStatus.ACTIVE}, LoanStatus.RETURNED)
