from .context import AppContext
from .menu import Menu, MenuItem
from .texts import (
    MENU_REPORTS,
    PROMPT_PERIOD_END,
    PROMPT_PERIOD_START,
    PROMPT_TOP_LIMIT,
    REPORT_LINE,
    REPORTS_ITEMS,
    TITLE_POPULAR,
)


def show_summary(context: AppContext) -> None:
    """Показывает сводку о состоянии библиотеки."""
    for label, value in context.library.summary().items():
        context.io.say(REPORT_LINE.format(label=label, value=value))


def show_period_report(context: AppContext) -> None:
    """Формирует отчёт за период."""
    start = context.io.ask_date(PROMPT_PERIOD_START)
    end = context.io.ask_date(PROMPT_PERIOD_END)
    report = context.library.generate_report(start, end)
    for label, value in report.summary().items():
        context.io.say(REPORT_LINE.format(label=label, value=value))


def show_popular_items(context: AppContext) -> None:
    """Показывает самые востребованные издания за период."""
    start = context.io.ask_date(PROMPT_PERIOD_START)
    end = context.io.ask_date(PROMPT_PERIOD_END)
    limit = context.io.ask_int(PROMPT_TOP_LIMIT)
    report = context.library.generate_report(start, end)
    context.io.say(TITLE_POPULAR)
    for title, count in report.popular_items(limit):
        context.io.say(REPORT_LINE.format(label=title, value=count))


REPORT_ACTIONS = (show_summary, show_period_report, show_popular_items)


def build_menu() -> Menu:
    """Собирает меню раздела «Отчёты»."""
    items = [MenuItem(label, action) for label, action in zip(REPORTS_ITEMS, REPORT_ACTIONS)]
    return Menu(MENU_REPORTS, items)
