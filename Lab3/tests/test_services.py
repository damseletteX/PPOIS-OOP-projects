from datetime import time, timedelta

import pytest

from library_system import (
    ActiveLoansError,
    CopyCondition,
    IdKind,
    ItemNotFoundError,
    LibraryReport,
    PaymentMethod,
    ReaderNotFoundError,
    StaffNotFoundError,
    ValidationError,
)
from library_system.ids import IdGenerator
from library_system.timeutils import hours_between, intervals_overlap, time_to_hours

from .factories import TODAY, make_librarian, make_reader

DAY = timedelta(days=1)


def issue(library):
    copy = library.receive_copy("IT-0001", "BR-0001", 20.0, TODAY)
    return library.issue_loan("RD-0001", copy.inventory_number, "ST-0001", TODAY)


def test_id_generator():
    ids = IdGenerator()
    assert ids.next_id(IdKind.READER) == "RD-0001"
    assert ids.next_id(IdKind.READER) == "RD-0002"
    assert ids.next_id(IdKind.LOAN) == "LN-0001"
    assert ids.issued_count(IdKind.READER) == 2
    ids.reset(IdKind.READER)
    assert ids.issued_count(IdKind.READER) == 0


def test_time_helpers():
    assert time_to_hours(time(10, 30)) == 10.5
    assert hours_between(time(9, 0), time(11, 30)) == 2.5
    assert intervals_overlap(time(9, 0), time(11, 0), time(10, 0), time(12, 0))
    assert not intervals_overlap(time(9, 0), time(10, 0), time(10, 0), time(12, 0))


def test_reader_registry(library):
    registry = library.readers
    assert registry.get("RD-0001").name == "Иван Петров"
    assert registry.find_by_name("иван") and registry.count_active() == 1
    assert registry.history and registry.last_updated == TODAY
    with pytest.raises(ValidationError):
        registry.register(make_reader("RD-0001"), TODAY)
    with pytest.raises(ReaderNotFoundError):
        registry.get("RD-9999")


def test_reader_registry_unregister(library):
    issue(library)
    with pytest.raises(ActiveLoansError):
        library.readers.unregister("RD-0001", TODAY)
    library.return_loan("LN-0001", CopyCondition.GOOD, "ST-0001", TODAY)
    assert library.readers.unregister("RD-0001", TODAY).name == "Иван Петров"


def test_debtors_and_overdue_lists(library):
    loan = issue(library)
    late_day = loan.due_on + 6 * DAY
    assert library.readers.with_overdue(late_day)
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", late_day)
    assert library.readers.debtors() and not library.readers.with_overdue(late_day)


def test_staff_registry(library):
    registry = library.staff
    assert len(registry.librarians()) == 1 and registry.total_payroll() == 4500.0
    assert registry.get_director("ST-0002").name == "Ирина Волкова"
    assert len(registry.by_branch(library.get_branch("BR-0001"))) == 2
    with pytest.raises(StaffNotFoundError):
        registry.get_librarian("ST-0002")
    with pytest.raises(StaffNotFoundError):
        registry.get_director("ST-0001")
    with pytest.raises(StaffNotFoundError):
        registry.get("ST-9999")
    with pytest.raises(ValidationError):
        registry.hire(make_librarian("ST-0001"))


def test_staff_dismissal(library):
    dismissed = library.staff.dismiss("ST-0001")
    assert not dismissed.is_active and library.staff.members.get("ST-0001") is None
    assert dismissed not in library.get_branch("BR-0001").staff
    outsider = make_librarian("ST-0050")
    library.staff.hire(outsider)
    assert library.staff.dismiss("ST-0050") is outsider


def test_library_basics(library):
    assert library.get_branch("BR-0001").name == "Центральный"
    with pytest.raises(ItemNotFoundError):
        library.get_branch("BR-9")
    with pytest.raises(ItemNotFoundError):
        library.get_supplier("SP-9")
    with pytest.raises(ItemNotFoundError):
        library.get_order("PO-9")
    assert library.readers.get("RD-0001").card is not None


def test_library_pay_fine_flow(library):
    loan = issue(library)
    library.return_loan(loan.loan_id, CopyCondition.DAMAGED, "ST-0001", TODAY + DAY)
    fine = library.readers.get("RD-0001").fines[0]
    payment = library.pay_fine("RD-0001", fine.fine_id, 5.0, PaymentMethod.CASH, TODAY + DAY)
    assert payment in library.payments and fine.balance() == 5.0
    with pytest.raises(ItemNotFoundError):
        library.find_fine("RD-0001", "FN-9999")


def test_library_purchase_flow(library):
    order = library.create_order("SP-0001", TODAY)
    library.add_order_line(order.order_id, "IT-0001", 2, 15.0)
    library.approve_order(order.order_id, "ST-0002")
    assert library.budget.remaining() == 970.0 and library.budget.orders == [order]
    library.send_order(order.order_id, TODAY)
    copies = library.receive_order(order.order_id, "BR-0001", TODAY + 5 * DAY)
    assert len(copies) == 2 and order.status.value == "получен"


def test_library_cancel_order_releases_budget(library):
    order = library.create_order("SP-0001", TODAY)
    library.add_order_line(order.order_id, "IT-0001", 2, 15.0)
    library.approve_order(order.order_id, "ST-0002")
    library.cancel_order(order.order_id)
    assert library.budget.remaining() == 1000.0


def test_library_cancel_draft_keeps_budget(library):
    order = library.create_order("SP-0001", TODAY)
    library.cancel_order(order.order_id)
    assert library.budget.remaining() == 1000.0


def test_receive_order_skips_received_lines(library):
    order = library.create_order("SP-0001", TODAY)
    library.add_order_line(order.order_id, "IT-0001", 1, 15.0)
    library.add_order_line(order.order_id, "IT-0001", 1, 15.0)
    library.approve_order(order.order_id, "ST-0002")
    library.send_order(order.order_id, TODAY)
    order.receive_line(order.lines[0], 1)
    assert len(library.receive_order(order.order_id, "BR-0001", TODAY)) == 1


def test_purchase_without_budget():
    from library_system import BudgetExceededError, Library

    from .factories import make_director

    empty = Library("Пустая", "Адрес")
    with pytest.raises(BudgetExceededError):
        empty.require_budget()
    assert empty.set_budget(2026, 10.0) is empty.budget
    assert make_director()


def test_report_metrics(library):
    loan = issue(library)
    late_day = loan.due_on + 6 * DAY
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", late_day)
    fine = library.readers.get("RD-0001").fines[0]
    library.pay_fine("RD-0001", fine.fine_id, 1.0, PaymentMethod.CARD, late_day)
    report = library.generate_report(TODAY, late_day)
    assert report.overdue_count() == 1 and report.total_fines() == 2.5
    assert report.total_collected() == 1.0 and report.average_loan_days() == 27.0
    assert report.popular_items(3) == [("Чистый код", 1)]
    assert len(report.summary()) == 6


def test_report_edge_cases(library):
    report = library.generate_report(TODAY, TODAY)
    assert report.average_loan_days() == 0.0 and report.popular_items(3) == []
    with pytest.raises(ValidationError):
        library.generate_report(TODAY + DAY, TODAY)
    assert LibraryReport


def test_library_summary(library):
    issue(library)
    summary = library.summary()
    assert summary["Изданий в каталоге"] == "1" and summary["Выдач на руках"] == "1"


def test_services_seat_event_and_request(library):
    services = library.services
    booking = services.book_seat("BR-0001", "RM-0001", "RD-0001", TODAY, time(10, 0), time(12, 0))
    assert booking.is_active
    event = services.schedule_event("Встреча", TODAY + DAY, "BR-0001", "RM-0001", "ST-0001", 5)
    services.register_for_event(event.event_id, "RD-0001", TODAY)
    assert services.get_event(event.event_id).attendees_count() == 1
    request = services.request_interlibrary("RD-0001", "Редкая книга", "Нац. библиотека", TODAY)
    services.approve_request(request.request_id, "ST-0001", TODAY + 7 * DAY)
    assert request.fee > 0
    with pytest.raises(ItemNotFoundError):
        services.get_event("EV-9")
    with pytest.raises(ItemNotFoundError):
        services.approve_request("IR-9", "ST-0001", TODAY)


def test_services_subscription_donation_inventory_review(library):
    from library_system import Magazine

    library.catalog.add_item(Magazine("IT-0005", "Наука", 2026, "0028-1263", 1))
    services = library.services
    subscription = services.subscribe("RD-0001", "IT-0005", 3, TODAY)
    assert subscription.is_active_on(TODAY)
    with pytest.raises(ItemNotFoundError):
        services.subscribe("RD-0001", "IT-0001", 3, TODAY)
    donation = services.accept_donation("RD-0001", 15.0, "ST-0001", TODAY)
    anonymous = services.accept_donation(None, 5.0, "ST-0001", TODAY)
    assert donation.donor is not None and anonymous.is_anonymous()
    copy = library.receive_copy("IT-0001", "BR-0001", 20.0, TODAY)
    audit = services.run_inventory("BR-0001", "ST-0001", [copy.inventory_number], TODAY)
    assert audit.is_complete() and services.audits == [audit]
    review = services.add_review("RD-0001", "IT-0001", 5, "Отлично", TODAY)
    assert review in library.catalog.get_item("IT-0001").reviews
