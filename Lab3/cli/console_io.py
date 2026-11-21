from collections.abc import Callable, Iterable, Sequence
from datetime import date, time
from enum import Enum
from typing import TypeVar

from .texts import (
    ERROR_INVALID_CHOICE,
    ERROR_INVALID_DATE,
    ERROR_INVALID_NUMBER,
    ERROR_INVALID_TIME,
    OPTION_FIRST_NUMBER,
    OPTION_FORMAT,
)

ParsedValue = TypeVar("ParsedValue")
EnumMember = TypeVar("EnumMember", bound=Enum)


class ConsoleIO:
    """Ввод и вывод в консоль; функции ввода и вывода можно подменить в тестах."""

    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ):
        self.input_func = input_func
        self.output_func = output_func

    def say(self, text: str = "") -> None:
        """Выводит строку."""
        self.output_func(text)

    def say_lines(self, lines: Iterable[str]) -> None:
        """Выводит несколько строк."""
        for line in lines:
            self.say(line)

    def ask(self, prompt: str) -> str:
        """Запрашивает строку и обрезает пробелы."""
        return self.input_func(prompt).strip()

    def ask_int(self, prompt: str) -> int:
        """Запрашивает целое число, пока ввод не станет корректным."""
        return self._ask_parsed(prompt, int, ERROR_INVALID_NUMBER)

    def ask_float(self, prompt: str) -> float:
        """Запрашивает вещественное число."""
        return self._ask_parsed(prompt, float, ERROR_INVALID_NUMBER)

    def ask_date(self, prompt: str) -> date:
        """Запрашивает дату в формате ГГГГ-ММ-ДД."""
        return self._ask_parsed(prompt, date.fromisoformat, ERROR_INVALID_DATE)

    def ask_time(self, prompt: str) -> time:
        """Запрашивает время в формате ЧЧ:ММ."""
        return self._ask_parsed(prompt, time.fromisoformat, ERROR_INVALID_TIME)

    def choose(self, prompt: str, options: Sequence[str]) -> int:
        """Показывает нумерованные варианты и возвращает индекс выбранного."""
        for number, option in enumerate(options, start=OPTION_FIRST_NUMBER):
            self.say(OPTION_FORMAT.format(number=number, option=option))
        while True:
            index = self.ask_int(prompt) - OPTION_FIRST_NUMBER
            if 0 <= index < len(options):
                return index
            self.say(ERROR_INVALID_CHOICE)

    def choose_enum(self, prompt: str, enum_class: type[EnumMember]) -> EnumMember:
        """Предлагает выбрать значение перечисления."""
        members = list(enum_class)
        index = self.choose(prompt, [member.value for member in members])
        return members[index]

    def _ask_parsed(
        self, prompt: str, parser: Callable[[str], ParsedValue], error_text: str
    ) -> ParsedValue:
        while True:
            try:
                return parser(self.ask(prompt))
            except ValueError:
                self.say(error_text)
