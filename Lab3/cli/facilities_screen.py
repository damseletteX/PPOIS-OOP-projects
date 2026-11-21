from library_system import ReadingRoom

from .context import AppContext
from .formatters import describe_event
from .menu import Menu, MenuItem
from .texts import (
    FACILITIES_ITEMS,
    FORMAT_BRANCH,
    FORMAT_ROOM,
    MENU_FACILITIES,
    MSG_BOOKED,
    MSG_BRANCH_OPENED,
    MSG_EVENT_REGISTERED,
    MSG_EVENT_SCHEDULED,
    MSG_REQUEST_CREATED,
    MSG_SUBSCRIBED,
    PROMPT_ADDRESS,
    PROMPT_DATE,
    PROMPT_END_TIME,
    PROMPT_EVENT_ID,
    PROMPT_MAX_PARTICIPANTS,
    PROMPT_MONTHS,
    PROMPT_NAME,
    PROMPT_PARTNER,
    PROMPT_PHONE,
    PROMPT_ROOM_ID,
    PROMPT_START_TIME,
    PROMPT_TITLE,
)


def open_branch(context: AppContext) -> None:
    """Открывает новый филиал."""
    io = context.io
    branch = context.library.open_branch(
        io.ask(PROMPT_NAME), io.ask(PROMPT_ADDRESS), io.ask(PROMPT_PHONE)
    )
    io.say(MSG_BRANCH_OPENED.format(branch_id=branch.branch_id))


def list_branches(context: AppContext) -> None:
    """Выводит филиалы и их читальные залы."""
    for branch in context.library.branches.values():
        context.io.say(
            FORMAT_BRANCH.format(
                branch_id=branch.branch_id, name=branch.name, staff=branch.staff_count()
            )
        )
        context.io.say_lines(describe_room(room) for room in branch.rooms)


def describe_room(room: ReadingRoom) -> str:
    """Краткое описание читального зала."""
    return FORMAT_ROOM.format(room_id=room.room_id, name=room.name, seats=room.seats_total)


def book_seat(context: AppContext) -> None:
    """Бронирует место в читальном зале."""
    io = context.io
    branch = context.ask_branch()
    room_id = io.ask(PROMPT_ROOM_ID)
    reader = context.ask_reader()
    booking_date = io.ask_date(PROMPT_DATE)
    start, end = io.ask_time(PROMPT_START_TIME), io.ask_time(PROMPT_END_TIME)
    booking = context.library.services.book_seat(
        branch.branch_id, room_id, reader.reader_id, booking_date, start, end
    )
    io.say(MSG_BOOKED.format(booking_id=booking.booking_id, hours=booking.duration_hours()))


def schedule_event(context: AppContext) -> None:
    """Планирует мероприятие."""
    io = context.io
    branch = context.ask_branch()
    title = io.ask(PROMPT_TITLE)
    event_date = io.ask_date(PROMPT_DATE)
    room_id = io.ask(PROMPT_ROOM_ID)
    organizer_id = context.ask_staff_id()
    limit = io.ask_int(PROMPT_MAX_PARTICIPANTS)
    event = context.library.services.schedule_event(
        title, event_date, branch.branch_id, room_id, organizer_id, limit
    )
    io.say(MSG_EVENT_SCHEDULED.format(event_id=event.event_id))


def register_for_event(context: AppContext) -> None:
    """Записывает читателя на мероприятие."""
    event_id = context.io.ask(PROMPT_EVENT_ID)
    reader = context.ask_reader()
    context.library.services.register_for_event(event_id, reader.reader_id, context.today)
    context.io.say(MSG_EVENT_REGISTERED)


def list_events(context: AppContext) -> None:
    """Выводит запланированные мероприятия."""
    events = context.library.services.events.values()
    context.io.say_lines(describe_event(event) for event in events)


def request_interlibrary(context: AppContext) -> None:
    """Оформляет запрос на издание из другой библиотеки."""
    io = context.io
    reader = context.ask_reader()
    title = io.ask(PROMPT_TITLE)
    request = context.library.services.request_interlibrary(
        reader.reader_id, title, io.ask(PROMPT_PARTNER), context.today
    )
    io.say(MSG_REQUEST_CREATED.format(request_id=request.request_id))


def subscribe(context: AppContext) -> None:
    """Оформляет подписку на журнал."""
    reader = context.ask_reader()
    magazine_id = context.ask_item_id()
    months = context.io.ask_int(PROMPT_MONTHS)
    subscription = context.library.services.subscribe(
        reader.reader_id, magazine_id, months, context.today
    )
    context.io.say(MSG_SUBSCRIBED.format(end_on=subscription.end_on.isoformat()))


FACILITIES_ACTIONS = (
    open_branch,
    list_branches,
    book_seat,
    schedule_event,
    register_for_event,
    list_events,
    request_interlibrary,
    subscribe,
)


def build_menu() -> Menu:
    """Собирает меню раздела «Филиалы и услуги»."""
    items = [MenuItem(label, action) for label, action in zip(FACILITIES_ITEMS, FACILITIES_ACTIONS)]
    return Menu(MENU_FACILITIES, items)
