from datetime import date

from library_system import Library

from . import (
    catalog_screen,
    circulation_screen,
    facilities_screen,
    finance_screen,
    readers_screen,
    reports_screen,
    staff_screen,
)
from .console_io import ConsoleIO
from .context import AppContext
from .demo_data import DEMO_LIBRARY_ADDRESS, DEMO_LIBRARY_NAME, load_demo_data
from .menu import Menu, MenuItem
from .texts import MAIN_ITEMS, MENU_MAIN, MSG_DEMO_LOADED, MSG_WELCOME


def load_demo(context: AppContext) -> None:
    """Загружает демонстрационные данные."""
    load_demo_data(context.library, context.today)
    context.io.say(MSG_DEMO_LOADED)


def build_main_menu() -> Menu:
    """Собирает главное меню."""
    sections = (
        readers_screen.build_menu(),
        catalog_screen.build_menu(),
        circulation_screen.build_menu(),
        finance_screen.build_menu(),
        facilities_screen.build_menu(),
        staff_screen.build_menu(),
        reports_screen.build_menu(),
    )
    items = [MenuItem(label, menu.run) for label, menu in zip(MAIN_ITEMS, sections)]
    items.append(MenuItem(MAIN_ITEMS[-1], load_demo))
    return Menu(MENU_MAIN, items)


def run(io: ConsoleIO | None = None, today: date | None = None) -> None:
    """Запускает консольное приложение."""
    console = io or ConsoleIO()
    library = Library(DEMO_LIBRARY_NAME, DEMO_LIBRARY_ADDRESS)
    context = AppContext(library, console, today or date.today())
    console.say(MSG_WELCOME.format(name=library.name))
    build_main_menu().run(context)
