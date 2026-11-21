from dataclasses import dataclass
from datetime import date

from library_system import Branch, Library, Reader

from .console_io import ConsoleIO
from .texts import PROMPT_BRANCH_ID, PROMPT_ITEM_ID, PROMPT_READER_ID, PROMPT_STAFF_ID


@dataclass
class AppContext:
    """Общие объекты приложения: библиотека, ввод-вывод и текущая дата."""

    library: Library
    io: ConsoleIO
    today: date

    def ask_reader(self) -> Reader:
        """Запрашивает идентификатор и возвращает читателя."""
        return self.library.readers.get(self.io.ask(PROMPT_READER_ID))

    def ask_item_id(self) -> str:
        """Запрашивает идентификатор издания."""
        return self.io.ask(PROMPT_ITEM_ID)

    def ask_staff_id(self) -> str:
        """Запрашивает табельный номер сотрудника."""
        return self.io.ask(PROMPT_STAFF_ID)

    def ask_branch(self) -> Branch:
        """Показывает филиалы и возвращает выбранный."""
        for branch in self.library.branches.values():
            self.io.say(f"  {branch.branch_id}: {branch.name}")
        return self.library.get_branch(self.io.ask(PROMPT_BRANCH_ID))
