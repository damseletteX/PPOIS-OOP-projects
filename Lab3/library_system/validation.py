"""Функции проверки входных данных доменных объектов."""

from enum import Enum

from .constants import (
    EMAIL_MARKER,
    ISBN_EVEN_WEIGHT,
    ISBN_LENGTH,
    ISBN_MODULUS,
    ISBN_ODD_WEIGHT,
    ISBN_SEPARATOR,
    RULE_EMAIL,
    RULE_ISBN,
    RULE_NON_NEGATIVE,
    RULE_NOT_EMPTY,
    RULE_POSITIVE,
    RULE_RANGE,
)
from .exceptions import InvalidStatusTransitionError, ValidationError


def require_text(value: str, field_name: str) -> str:
    """Возвращает очищенную непустую строку."""
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(field_name, RULE_NOT_EMPTY)
    return cleaned


def require_positive(value: float, field_name: str) -> float:
    """Проверяет, что число больше нуля."""
    if value <= 0:
        raise ValidationError(field_name, RULE_POSITIVE)
    return value


def require_non_negative(value: float, field_name: str) -> float:
    """Проверяет, что число не отрицательно."""
    if value < 0:
        raise ValidationError(field_name, RULE_NON_NEGATIVE)
    return value


def require_in_range(value: float, low: float, high: float, field_name: str) -> float:
    """Проверяет, что число лежит в закрытом диапазоне."""
    if not low <= value <= high:
        raise ValidationError(field_name, RULE_RANGE.format(low=low, high=high))
    return value


def require_email(value: str, field_name: str) -> str:
    """Проверяет простой формат адреса электронной почты (пустая строка допустима)."""
    cleaned = value.strip()
    if cleaned and EMAIL_MARKER not in cleaned:
        raise ValidationError(field_name, RULE_EMAIL)
    return cleaned


def is_valid_isbn(isbn: str) -> bool:
    """Проверяет контрольную сумму ISBN-13."""
    if len(isbn) != ISBN_LENGTH or not isbn.isdigit():
        return False
    weights = (ISBN_ODD_WEIGHT, ISBN_EVEN_WEIGHT)
    total = sum(
        int(digit) * weights[position % len(weights)] for position, digit in enumerate(isbn)
    )
    return total % ISBN_MODULUS == 0


def require_isbn(value: str, field_name: str) -> str:
    """Возвращает ISBN без дефисов, если он корректен."""
    cleaned = value.replace(ISBN_SEPARATOR, "").strip()
    if not is_valid_isbn(cleaned):
        raise ValidationError(field_name, RULE_ISBN)
    return cleaned


def ensure_transition(entity: str, current: Enum, allowed: set, target: Enum) -> None:
    """Проверяет допустимость смены статуса и бросает исключение при нарушении."""
    if current not in allowed:
        raise InvalidStatusTransitionError(entity, current.value, target.value)
