from collections.abc import Callable
from dataclasses import dataclass

from library_system.exceptions import LibraryError

from .context import AppContext
from .texts import ERROR_INVALID_CHOICE, ERROR_PREFIX, EXIT_CHOICE, EXIT_LABEL, PROMPT_CHOICE


@dataclass(frozen=True)
class MenuItem:
    """Пункт меню: подпись и действие."""

    label: str
    action: Callable[[AppContext], None]


class Menu:
    """Меню с выбором пункта по номеру; ошибки предметной области выводятся в консоль."""

    def __init__(self, title: str, items: list[MenuItem]):
        self.title = title
        self.items = items

    def run(self, context: AppContext) -> None:
        """Показывает меню и выполняет выбранные действия до выхода."""
        while True:
            self._show(context)
            choice = context.io.ask_int(PROMPT_CHOICE)
            if choice == EXIT_CHOICE:
                return
            self._execute(choice, context)

    def _show(self, context: AppContext) -> None:
        context.io.say()
        context.io.say(self.title)
        for number, item in enumerate(self.items, start=EXIT_CHOICE + 1):
            context.io.say(f"  {number}. {item.label}")
        context.io.say(f"  {EXIT_CHOICE}. {EXIT_LABEL}")

    def _execute(self, choice: int, context: AppContext) -> None:
        index = choice - EXIT_CHOICE - 1
        if not 0 <= index < len(self.items):
            context.io.say(ERROR_INVALID_CHOICE)
            return
        try:
            self.items[index].action(context)
        except LibraryError as error:
            context.io.say(f"{ERROR_PREFIX}{error}")
