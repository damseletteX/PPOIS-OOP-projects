"""Вспомогательные функции для работы со временем."""

from datetime import time

from .constants import CURRENCY_DIGITS, MINUTES_IN_HOUR


def time_to_hours(moment: time) -> float:
    """Переводит время суток в часы с дробной частью."""
    return moment.hour + moment.minute / MINUTES_IN_HOUR


def hours_between(start: time, end: time) -> float:
    """Возвращает длительность интервала в часах."""
    return round(time_to_hours(end) - time_to_hours(start), CURRENCY_DIGITS)


def intervals_overlap(
    first_start: time, first_end: time, second_start: time, second_end: time
) -> bool:
    """Проверяет пересечение двух интервалов времени."""
    return first_start < second_end and second_start < first_end
