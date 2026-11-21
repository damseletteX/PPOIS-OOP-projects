from datetime import date

from library_system import ChildReader, MembershipPlan, Reader, StudentReader
from library_system.enums import IdKind

from .context import AppContext
from .formatters import describe_fine, describe_loan, describe_reader
from .menu import Menu, MenuItem
from .texts import (
    MENU_READERS,
    MSG_CARD_BLOCKED,
    MSG_CARD_RENEWED,
    MSG_CARD_UNBLOCKED,
    MSG_NO_READERS,
    MSG_PLAN_CHANGED,
    MSG_READER_REGISTERED,
    MSG_READER_REMOVED,
    PROMPT_BIRTH_DATE,
    PROMPT_COURSE,
    PROMPT_EMAIL,
    PROMPT_NAME,
    PROMPT_PHONE,
    PROMPT_PLAN,
    PROMPT_READER_KIND,
    PROMPT_REASON,
    PROMPT_SCHOOL,
    PROMPT_STUDENT_NUMBER,
    PROMPT_UNIVERSITY,
    READER_KINDS,
    READERS_ITEMS,
    TITLE_FINES,
    TITLE_LOANS,
)


def read_person(context: AppContext) -> tuple[str, str, date, str]:
    """Запрашивает общие данные человека: имя, телефон, дату рождения, почту."""
    io = context.io
    name = io.ask(PROMPT_NAME)
    phone = io.ask(PROMPT_PHONE)
    birth_date = io.ask_date(PROMPT_BIRTH_DATE)
    return name, phone, birth_date, io.ask(PROMPT_EMAIL)


def build_regular(context: AppContext, reader_id: str) -> Reader:
    """Создаёт обычного читателя."""
    name, phone, birth_date, email = read_person(context)
    return Reader(reader_id, name, phone, birth_date, context.today, email)


def build_student(context: AppContext, reader_id: str) -> StudentReader:
    """Создаёт читателя-студента."""
    name, phone, birth_date, email = read_person(context)
    student_number = context.io.ask(PROMPT_STUDENT_NUMBER)
    university = context.io.ask(PROMPT_UNIVERSITY)
    course = context.io.ask_int(PROMPT_COURSE)
    return StudentReader(
        reader_id, name, phone, birth_date, context.today, student_number, university, course, email
    )


def build_child(context: AppContext, reader_id: str) -> ChildReader:
    """Создаёт читателя-ребёнка с опекуном."""
    name, phone, birth_date, email = read_person(context)
    guardian = context.ask_reader()
    school = context.io.ask(PROMPT_SCHOOL)
    child = ChildReader(reader_id, name, phone, birth_date, context.today, guardian, school, email)
    child.grant_consent()
    return child


READER_BUILDERS = (build_regular, build_student, build_child)


def register_reader(context: AppContext) -> None:
    """Регистрирует нового читателя и выдаёт ему билет."""
    kind = context.io.choose(PROMPT_READER_KIND, READER_KINDS)
    reader_id = context.library.ids.next_id(IdKind.READER)
    reader = READER_BUILDERS[kind](context, reader_id)
    context.library.register_reader(reader, context.today)
    card_number = reader.card.card_number if reader.card else ""
    context.io.say(MSG_READER_REGISTERED.format(reader_id=reader_id, card=card_number))


def list_readers(context: AppContext) -> None:
    """Выводит список читателей."""
    readers = list(context.library.readers.readers.values())
    if not readers:
        context.io.say(MSG_NO_READERS)
    context.io.say_lines(describe_reader(reader) for reader in readers)


def show_reader(context: AppContext) -> None:
    """Показывает карточку читателя: выдачи и штрафы."""
    reader = context.ask_reader()
    context.io.say(describe_reader(reader))
    context.io.say(TITLE_LOANS)
    context.io.say_lines(describe_loan(loan) for loan in reader.active_loans())
    context.io.say(TITLE_FINES)
    context.io.say_lines(describe_fine(fine) for fine in reader.fines)


def change_plan(context: AppContext) -> None:
    """Меняет тариф абонемента читателя."""
    reader = context.ask_reader()
    plan = context.io.choose_enum(PROMPT_PLAN, MembershipPlan)
    surcharge = reader.change_plan(plan)
    context.io.say(MSG_PLAN_CHANGED.format(plan=plan.value, surcharge=surcharge))


def block_card(context: AppContext) -> None:
    """Блокирует читательский билет."""
    reader = context.ask_reader()
    reader.block_card(context.io.ask(PROMPT_REASON))
    context.io.say(MSG_CARD_BLOCKED)


def unblock_card(context: AppContext) -> None:
    """Снимает блокировку билета."""
    context.ask_reader().unblock_card()
    context.io.say(MSG_CARD_UNBLOCKED)


def renew_card(context: AppContext) -> None:
    """Продлевает читательский билет."""
    card = context.ask_reader().renew_card(context.today)
    context.io.say(MSG_CARD_RENEWED.format(expires_on=card.expires_on.isoformat()))


def unregister_reader(context: AppContext) -> None:
    """Снимает читателя с учёта."""
    reader = context.ask_reader()
    context.library.readers.unregister(reader.reader_id, context.today)
    context.io.say(MSG_READER_REMOVED)


READER_ACTIONS = (
    register_reader,
    list_readers,
    show_reader,
    change_plan,
    block_card,
    unblock_card,
    renew_card,
    unregister_reader,
)


def build_menu() -> Menu:
    """Собирает меню раздела «Читатели»."""
    items = [MenuItem(label, action) for label, action in zip(READERS_ITEMS, READER_ACTIONS)]
    return Menu(MENU_READERS, items)
