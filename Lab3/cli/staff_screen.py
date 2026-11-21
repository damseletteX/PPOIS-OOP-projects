from library_system import Librarian
from library_system.enums import IdKind

from .context import AppContext
from .formatters import describe_staff
from .menu import Menu, MenuItem
from .readers_screen import read_person
from .texts import (
    MENU_STAFF,
    MSG_PAYROLL,
    MSG_STAFF_HIRED,
    PROMPT_SALARY,
    STAFF_ITEMS,
)


def hire_librarian(context: AppContext) -> None:
    """Принимает библиотекаря на работу в выбранный филиал."""
    name, phone, birth_date, email = read_person(context)
    salary = context.io.ask_float(PROMPT_SALARY)
    branch = context.ask_branch()
    staff_id = context.library.ids.next_id(IdKind.STAFF)
    librarian = Librarian(staff_id, name, phone, birth_date, salary, context.today, email=email)
    context.library.hire_staff(librarian, branch.branch_id)
    context.io.say(MSG_STAFF_HIRED.format(staff_id=staff_id))


def list_staff(context: AppContext) -> None:
    """Выводит сотрудников."""
    members = context.library.staff.members.values()
    context.io.say_lines(describe_staff(member) for member in members)


def show_payroll(context: AppContext) -> None:
    """Показывает месячный фонд оплаты труда."""
    context.io.say(MSG_PAYROLL.format(total=context.library.staff.total_payroll()))


STAFF_ACTIONS = (hire_librarian, list_staff, show_payroll)


def build_menu() -> Menu:
    """Собирает меню раздела «Сотрудники»."""
    items = [MenuItem(label, action) for label, action in zip(STAFF_ITEMS, STAFF_ACTIONS)]
    return Menu(MENU_STAFF, items)
