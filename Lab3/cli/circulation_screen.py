from library_system import CopyCondition

from .context import AppContext
from .formatters import describe_loan, describe_notification
from .menu import Menu, MenuItem
from .texts import (
    CIRCULATION_ITEMS,
    MENU_CIRCULATION,
    MSG_LOAN_ISSUED,
    MSG_LOAN_RENEWED,
    MSG_LOST_REPORTED,
    MSG_NO_OVERDUE,
    MSG_RESERVED,
    MSG_RETURNED,
    MSG_RETURNED_WITH_FINES,
    PROMPT_CONDITION,
    PROMPT_INVENTORY_NUMBER,
    PROMPT_LOAN_ID,
    PROMPT_STAFF_ID,
)


def issue_loan(context: AppContext) -> None:
    """Выдаёт экземпляр читателю."""
    io = context.io
    reader = context.ask_reader()
    inventory_number = io.ask(PROMPT_INVENTORY_NUMBER)
    librarian_id = io.ask(PROMPT_STAFF_ID)
    loan = context.library.issue_loan(
        reader.reader_id, inventory_number, librarian_id, context.today
    )
    io.say(MSG_LOAN_ISSUED.format(loan_id=loan.loan_id, due_on=loan.due_on.isoformat()))


def return_loan(context: AppContext) -> None:
    """Принимает издание обратно."""
    io = context.io
    loan_id = io.ask(PROMPT_LOAN_ID)
    condition = io.choose_enum(PROMPT_CONDITION, CopyCondition)
    librarian_id = io.ask(PROMPT_STAFF_ID)
    record = context.library.return_loan(loan_id, condition, librarian_id, context.today)
    fines = [fine for fine in context.library.loan_desk.fines if fine.loan is record.loan]
    io.say(MSG_RETURNED_WITH_FINES.format(count=len(fines)) if fines else MSG_RETURNED)


def renew_loan(context: AppContext) -> None:
    """Продлевает выдачу."""
    io = context.io
    renewal = context.library.renew_loan(
        io.ask(PROMPT_LOAN_ID), io.ask(PROMPT_STAFF_ID), context.today
    )
    io.say(MSG_LOAN_RENEWED.format(due_on=renewal.new_due_on.isoformat()))


def reserve_item(context: AppContext) -> None:
    """Бронирует издание, которого сейчас нет в наличии."""
    reader = context.ask_reader()
    reservation = context.library.reserve_item(
        reader.reader_id, context.ask_item_id(), context.today
    )
    waiting_list = context.library.loan_desk.waiting_list_for(reservation.item)
    position = waiting_list.position_of(reader)
    context.io.say(MSG_RESERVED.format(position=position))


def report_lost(context: AppContext) -> None:
    """Оформляет утрату издания."""
    report = context.library.report_lost(context.io.ask(PROMPT_LOAN_ID), context.today)
    context.io.say(MSG_LOST_REPORTED.format(amount=report.compensation_due()))


def list_overdue(context: AppContext) -> None:
    """Выводит просроченные выдачи."""
    overdue = context.library.loan_desk.collect_overdue_loans(context.today)
    context.io.say_lines(describe_loan(loan) for loan in overdue)
    if not overdue:
        context.io.say(MSG_NO_OVERDUE)


def send_reminders(context: AppContext) -> None:
    """Рассылает напоминания должникам."""
    reminders = context.library.loan_desk.send_overdue_reminders(context.today)
    context.io.say_lines(describe_notification(item) for item in reminders)
    if not reminders:
        context.io.say(MSG_NO_OVERDUE)


CIRCULATION_ACTIONS = (
    issue_loan,
    return_loan,
    renew_loan,
    reserve_item,
    report_lost,
    list_overdue,
    send_reminders,
)


def build_menu() -> Menu:
    """Собирает меню раздела «Выдача и возврат»."""
    items = [
        MenuItem(label, action) for label, action in zip(CIRCULATION_ITEMS, CIRCULATION_ACTIONS)
    ]
    return Menu(MENU_CIRCULATION, items)
