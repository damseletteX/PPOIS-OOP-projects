from datetime import date, datetime, time, timedelta

import pytest

from library_system import (
    Branch,
    CapacityExceededError,
    InventoryAudit,
    LibraryEvent,
    OpeningHours,
    ReadingRoom,
    ReservationError,
    SeatBooking,
    Shelf,
    StaffShift,
    ValidationError,
)

from .factories import CLOSE_TIME, OPEN_TIME, PHONE, TODAY, make_copy, make_librarian, make_reader

SUNDAY = date(2026, 11, 22)
DAY = timedelta(days=1)


def make_room(seats=2):
    return ReadingRoom("RM-1", "Зал", seats, OpeningHours())


def make_branch():
    return Branch("BR-1", "Центральный", "ул. Ленина", PHONE, OpeningHours())


def test_opening_hours():
    hours = OpeningHours()
    assert hours.is_working_day(TODAY) and not hours.is_working_day(SUNDAY)
    assert hours.is_open_at(datetime(2026, 11, 21, 10, 0))
    assert not hours.is_open_at(datetime(2026, 11, 21, 18, 0))
    assert not hours.is_open_at(datetime(2026, 11, 22, 10, 0))
    assert hours.daily_hours() == 9.0 and hours.working_days_count() == 6
    assert hours.weekly_hours() == 54.0 and hours.next_working_day(TODAY) == date(2026, 11, 23)


def test_opening_hours_without_working_days():
    hours = OpeningHours(working_weekdays=frozenset())
    assert hours.next_working_day(TODAY) is None
    with pytest.raises(ValidationError):
        OpeningHours(time(18, 0), time(9, 0))


def test_shelf_capacity():
    shelf = Shelf("SH-1", 1)
    copy = make_copy()
    shelf.place_copy(copy)
    assert shelf.is_full() and shelf.free_slots() == 0 and shelf.occupancy_percent() == 100.0
    assert shelf.contains_item(copy.item) and copy.shelf is shelf
    with pytest.raises(CapacityExceededError):
        shelf.place_copy(make_copy(number="CP-2"))
    shelf.remove_copy(copy)
    shelf.remove_copy(copy)
    assert copy.shelf is None and not shelf.is_full()


def test_seat_booking_model():
    booking = SeatBooking("BK-1", make_reader(), make_room(), TODAY, OPEN_TIME, CLOSE_TIME)
    assert booking.duration_hours() == 2.0 and booking.is_within_hours(OpeningHours())
    assert booking.overlaps(TODAY, time(11, 0), time(13, 0))
    assert not booking.overlaps(TODAY, CLOSE_TIME, time(13, 0))
    assert not booking.overlaps(SUNDAY, OPEN_TIME, CLOSE_TIME)
    booking.cancel()
    assert not booking.overlaps(TODAY, OPEN_TIME, CLOSE_TIME)
    with pytest.raises(ValidationError):
        SeatBooking("BK-2", make_reader(), make_room(), TODAY, CLOSE_TIME, OPEN_TIME)


def test_reading_room_booking_limits():
    room = make_room(seats=1)
    booking = room.book_seat("BK-1", make_reader(), TODAY, OPEN_TIME, CLOSE_TIME)
    assert room.booked_seats(TODAY, OPEN_TIME, CLOSE_TIME) == 1 and room.is_full(
        TODAY, OPEN_TIME, CLOSE_TIME
    )
    with pytest.raises(CapacityExceededError):
        room.book_seat("BK-2", make_reader("RD-2"), TODAY, OPEN_TIME, CLOSE_TIME)
    room.cancel_booking(booking)
    assert room.free_seats(TODAY, OPEN_TIME, CLOSE_TIME) == 1 and room.bookings_on(TODAY) == []


def test_reading_room_closed_day():
    with pytest.raises(CapacityExceededError):
        make_room().book_seat("BK-1", make_reader(), SUNDAY, OPEN_TIME, CLOSE_TIME)


def test_event_registration_rules():
    room = make_room(seats=5)
    event = LibraryEvent("EV-1", "Встреча с автором", TODAY + DAY, room, make_librarian(), 1)
    reader = make_reader()
    registration = event.register_reader("RG-1", reader, TODAY)
    assert event.attendees_count() == 1 and event.is_full() and event.seats_left() == 0
    with pytest.raises(ReservationError):
        event.register_reader("RG-2", reader, TODAY)
    with pytest.raises(CapacityExceededError):
        event.register_reader("RG-3", make_reader("RD-2"), TODAY)
    registration.mark_attended()
    assert registration.attended and registration.is_active()
    event.cancel_registration(reader)
    event.cancel_registration(reader)
    registration.mark_attended()
    assert not registration.attended and event.seats_left() == 1


def test_event_cancel_and_capacity():
    room = make_room(seats=2)
    with pytest.raises(CapacityExceededError):
        LibraryEvent("EV-2", "Большое", TODAY, room, make_librarian(), 3)
    event = LibraryEvent("EV-3", "Лекция", TODAY, room, make_librarian(), 2)
    assert event.is_upcoming(TODAY) and not event.is_upcoming(TODAY + DAY)
    event.cancel_event()
    assert not event.is_upcoming(TODAY)
    with pytest.raises(ReservationError):
        event.register_reader("RG-1", make_reader(), TODAY)


def test_staff_shift_rules():
    staff = make_librarian()
    branch = make_branch()
    morning = StaffShift("SF-1", staff, branch, TODAY, time(9, 0), time(13, 0))
    evening = StaffShift("SF-2", staff, branch, TODAY, time(13, 0), time(18, 0))
    assert morning.duration_hours() == 4.0 and not morning.overlaps(evening)
    assert morning.overlaps(StaffShift("SF-3", staff, branch, TODAY, time(12, 0), time(14, 0)))
    assert morning.is_active_at(datetime(2026, 11, 21, 9, 30))
    assert not morning.is_active_at(datetime(2026, 11, 22, 9, 30))
    with pytest.raises(ValidationError):
        StaffShift("SF-4", staff, branch, TODAY, time(13, 0), time(9, 0))


def test_branch_staff_and_shelves():
    branch = make_branch()
    staff = make_librarian()
    branch.hire(staff)
    branch.hire(staff)
    assert branch.staff_count() == 1 and staff.branch is branch and branch.payroll() == 1500.0
    branch.set_manager(staff)
    assert branch.manager is staff
    branch.dismiss(staff)
    assert branch.manager is None and branch.staff_count() == 0
    with pytest.raises(ValidationError):
        branch.set_manager(staff)


def test_branch_rooms_and_capacity():
    branch = make_branch()
    room = make_room()
    branch.add_room(room)
    shelf = Shelf("SH-1", 1)
    branch.add_shelf(shelf)
    assert branch.get_room("RM-1") is room and branch.total_capacity() == 1
    assert branch.is_open_at(datetime(2026, 11, 21, 10, 0))
    assert branch.find_free_shelf() is shelf
    copy = make_copy()
    shelf.place_copy(copy)
    assert branch.all_copies() == [copy]
    with pytest.raises(CapacityExceededError):
        branch.find_free_shelf()


def test_branch_unknown_room():
    from library_system import ItemNotFoundError

    with pytest.raises(ItemNotFoundError):
        make_branch().get_room("RM-9")


def test_inventory_audit():
    branch = make_branch()
    shelf = Shelf("SH-1", 5)
    branch.add_shelf(shelf)
    found, missing = make_copy(number="CP-1"), make_copy(number="CP-2")
    shelf.place_copy(found)
    shelf.place_copy(missing)
    audit = InventoryAudit("AD-1", branch, make_librarian(), TODAY)
    audit.register_found(found)
    audit.register_found(found)
    audit.register_found(make_copy(number="CP-3"))
    assert audit.found_percent() == 50.0 and not audit.is_complete()
    assert audit.missing_copies() == [missing] and audit.mark_missing_as_lost() == 1
    assert missing.status.value == "утеряно"


def test_empty_inventory_is_complete():
    audit = InventoryAudit("AD-2", make_branch(), make_librarian(), TODAY)
    assert audit.found_percent() == 100.0 and audit.is_complete()
