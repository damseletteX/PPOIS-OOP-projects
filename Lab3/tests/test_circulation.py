from datetime import timedelta

import pytest

from library_system import (
    AgeRestrictionError,
    CopyCondition,
    FineReason,
    InterlibraryRequest,
    InvalidStatusTransitionError,
    ItemNotAvailableError,
    ItemNotFoundError,
    LoanLimitExceededError,
    LoanPolicy,
    LostItemReport,
    Magazine,
    Notification,
    OverdueLoansError,
    ReaderBlockedError,
    RenewalNotAllowedError,
    ReservationError,
    ReservationStatus,
    Subscription,
    UnpaidFineError,
    ValidationError,
)

from .factories import TODAY, make_book, make_copy, make_librarian, make_reader, make_student

DAY = timedelta(days=1)


def issue(library, reader_id="RD-0001", copy_number=None, on_date=TODAY):
    copy_number = (
        copy_number or library.receive_copy("IT-0001", "BR-0001", 20.0, on_date).inventory_number
    )
    return library.issue_loan(reader_id, copy_number, "ST-0001", on_date)


def test_policy_calculations():
    policy = LoanPolicy()
    reader, student, book = make_reader(), make_student(), make_book()
    assert policy.effective_loan_limit(reader) == 3
    assert policy.loan_period_for(student, book) == 28
    assert policy.due_date_for(reader, book, TODAY) == TODAY + 21 * DAY
    assert policy.blocks_borrowing(10.01) and not policy.blocks_borrowing(10.0)


def test_issue_and_return_on_time(library):
    loan = issue(library)
    assert loan.is_active() and loan.due_on == TODAY + 21 * DAY
    record = library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY + 5 * DAY)
    assert not loan.is_active() and not record.was_late() and loan.days_borrowed(TODAY) == 5
    assert library.readers.get("RD-0001").fines == []


def test_late_return_creates_fine(library):
    loan = issue(library)
    late_day = loan.due_on + 5 * DAY
    assert loan.is_overdue(late_day) and loan.days_overdue(late_day) == 5
    record = library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", late_day)
    fine = library.readers.get("RD-0001").fines[0]
    assert record.days_late() == 5 and fine.reason == FineReason.OVERDUE and fine.amount == 2.0


def test_damaged_return_creates_damage_fine(library):
    loan = issue(library)
    record = library.return_loan(loan.loan_id, CopyCondition.DAMAGED, "ST-0001", TODAY + DAY)
    record.add_note(" обложка ")
    assert record.is_damaged() and record.requires_repair() and record.notes == ["обложка"]
    assert library.readers.get("RD-0001").fines[0].reason == FineReason.DAMAGE


def test_double_return_is_rejected(library):
    loan = issue(library)
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY)
    with pytest.raises(InvalidStatusTransitionError):
        library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY)


def test_unknown_loan(library):
    with pytest.raises(ItemNotFoundError):
        library.loan_desk.find_loan("LN-9999")


def test_issue_requires_card_and_activity(library):
    reader = library.readers.get("RD-0001")
    reader.block_card("долг")
    with pytest.raises(ReaderBlockedError):
        issue(library)


def test_loan_limit(library):
    for _ in range(3):
        issue(library)
    with pytest.raises(LoanLimitExceededError):
        issue(library)


def test_overdue_blocks_new_loans(library):
    loan = issue(library)
    with pytest.raises(OverdueLoansError):
        issue(library, on_date=loan.due_on + DAY)


def test_unpaid_fines_block_new_loans(library):
    loan = issue(library)
    library.return_loan(loan.loan_id, CopyCondition.DAMAGED, "ST-0001", TODAY + DAY)
    library.loan_desk.fines[0].add_surcharge(20.0)
    with pytest.raises(UnpaidFineError):
        issue(library, on_date=TODAY + 2 * DAY)


def test_reading_room_only_items_are_not_loaned(library):
    magazine = Magazine("IT-0005", "Наука", 2026, "0028-1263", 1)
    library.catalog.add_item(magazine)
    copy = library.receive_copy("IT-0005", "BR-0001", 5.0, TODAY)
    with pytest.raises(ItemNotAvailableError):
        library.issue_loan("RD-0001", copy.inventory_number, "ST-0001", TODAY)


def test_age_restriction_on_issue(library):
    adult_book = make_book("IT-0007", "Для взрослых", age_limit=18)
    library.catalog.add_item(adult_book)
    library.receive_copy("IT-0007", "BR-0001", 5.0, TODAY)
    child = make_reader("RD-0003")
    child.birth_date = TODAY - 365 * 10 * DAY
    library.register_reader(child, TODAY)
    with pytest.raises(AgeRestrictionError):
        library.issue_loan("RD-0003", "CP-0001", "ST-0001", TODAY)


def test_unavailable_copy_is_rejected(library):
    loan = issue(library)
    library.register_reader(make_reader("RD-0004", with_card=False), TODAY)
    with pytest.raises(ItemNotAvailableError):
        library.issue_loan("RD-0004", loan.copy.inventory_number, "ST-0001", TODAY)


def test_renewal_extends_due_date(library):
    loan = issue(library)
    renewal = library.renew_loan(loan.loan_id, "ST-0001", TODAY + DAY)
    assert renewal.is_approved() and renewal.extra_days() == 7
    assert loan.due_on == TODAY + 28 * DAY and loan.renewals_count() == 1
    assert library.loan_desk.loan_policy.renewals_left(loan) == 1


def test_renewal_limit(library):
    loan = issue(library)
    library.renew_loan(loan.loan_id, "ST-0001", TODAY)
    library.renew_loan(loan.loan_id, "ST-0001", TODAY)
    with pytest.raises(RenewalNotAllowedError):
        library.renew_loan(loan.loan_id, "ST-0001", TODAY)


def test_renewal_denied_for_overdue_and_closed(library):
    loan = issue(library)
    with pytest.raises(RenewalNotAllowedError):
        library.renew_loan(loan.loan_id, "ST-0001", loan.due_on + DAY)
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY)
    with pytest.raises(RenewalNotAllowedError):
        library.renew_loan(loan.loan_id, "ST-0001", TODAY)


def test_renewal_denied_when_queue_exists(library):
    loan = issue(library)
    library.register_reader(make_reader("RD-0005", with_card=False), TODAY)
    library.reserve_item("RD-0005", "IT-0001", TODAY)
    with pytest.raises(RenewalNotAllowedError):
        library.renew_loan(loan.loan_id, "ST-0001", TODAY)


def test_reservation_queue_and_hold(library):
    loan = issue(library)
    library.register_reader(make_reader("RD-0005", with_card=False), TODAY)
    reservation = library.reserve_item("RD-0005", "IT-0001", TODAY)
    desk = library.loan_desk
    assert desk.waiting_list_for(reservation.item).position_of(reservation.reader) == 1
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY + DAY)
    assert reservation.status == ReservationStatus.READY and desk.notifications
    next_loan = library.issue_loan("RD-0005", loan.copy.inventory_number, "ST-0001", TODAY + DAY)
    assert reservation.status == ReservationStatus.FULFILLED and next_loan.is_active()


def test_reservation_not_allowed_when_available(library):
    library.receive_copy("IT-0001", "BR-0001", 20.0, TODAY)
    with pytest.raises(ReservationError):
        library.reserve_item("RD-0001", "IT-0001", TODAY)


def test_reservation_duplicate_and_limit(library):
    issue(library)
    library.reserve_item("RD-0001", "IT-0001", TODAY)
    with pytest.raises(ReservationError):
        library.reserve_item("RD-0001", "IT-0001", TODAY)


def test_cancel_ready_reservation_passes_copy_on(library):
    loan = issue(library)
    for reader_id in ("RD-0005", "RD-0006"):
        library.register_reader(make_reader(reader_id, with_card=False), TODAY)
    first = library.reserve_item("RD-0005", "IT-0001", TODAY)
    second = library.reserve_item("RD-0006", "IT-0001", TODAY)
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY)
    library.loan_desk.cancel_reservation(first, TODAY)
    assert first.status == ReservationStatus.CANCELLED
    assert second.status == ReservationStatus.READY


def test_cancel_queued_reservation(library):
    issue(library)
    reservation = library.reserve_item("RD-0001", "IT-0001", TODAY)
    library.loan_desk.cancel_reservation(reservation, TODAY)
    assert library.loan_desk.waiting_list_for(reservation.item).is_empty()


def test_expire_unclaimed_reservation(library):
    loan = issue(library)
    library.register_reader(make_reader("RD-0005", with_card=False), TODAY)
    reservation = library.reserve_item("RD-0005", "IT-0001", TODAY)
    library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0001", TODAY)
    assert library.loan_desk.expire_reservations(TODAY + 10 * DAY) == 1
    assert reservation.status == ReservationStatus.EXPIRED and loan.copy.is_available()


def test_report_lost_creates_compensation(library):
    loan = issue(library)
    report = library.report_lost(loan.loan_id, TODAY + DAY)
    assert report.compensation_due() == 45.0 and not report.is_compensated()
    assert report.days_since_report(TODAY + 3 * DAY) == 2 and "CP-0001" in report.description()
    library.find_fine("RD-0001", report.fine.fine_id).waive()
    assert report.is_compensated()


def test_overdue_listing_and_reminders(library):
    loan = issue(library)
    day = loan.due_on + DAY
    assert library.loan_desk.collect_overdue_loans(day) == [loan]
    reminders = library.loan_desk.send_overdue_reminders(day)
    assert len(reminders) == 1 and "Чистый код" in reminders[0].message


def test_reservation_status_changes():
    reader, book = make_reader(), make_book()
    from library_system import Reservation

    reservation = Reservation("RS-1", reader, book, TODAY)
    assert reservation.is_open() and reservation.days_until_expiry(TODAY) == 3
    reservation.extend(2)
    assert reservation.days_until_expiry(TODAY) == 5
    with pytest.raises(InvalidStatusTransitionError):
        reservation.fulfill()
    reservation.cancel()
    assert not reservation.is_open() and not reservation.expire_if_needed(TODAY + 30 * DAY)


def test_waiting_list_basics():
    from library_system import Reservation, WaitingList

    book = make_book()
    waiting = WaitingList(book, max_length=1)
    first = Reservation("RS-1", make_reader(), book, TODAY)
    assert waiting.is_empty() and waiting.enqueue(first) == 1
    with pytest.raises(ReservationError):
        waiting.enqueue(Reservation("RS-2", make_reader("RD-2"), book, TODAY))
    first.cancel()
    waiting.remove(first)
    assert waiting.size() == 0 and waiting.pop_next() is None


def test_waiting_list_skips_cancelled():
    from library_system import Reservation, WaitingList

    book = make_book()
    waiting = WaitingList(book)
    cancelled = Reservation("RS-1", make_reader(), book, TODAY)
    active = Reservation("RS-2", make_reader("RD-2"), book, TODAY)
    waiting.enqueue(cancelled)
    waiting.enqueue(active)
    cancelled.cancel()
    assert waiting.pop_next() is active


def test_interlibrary_flow():
    request = InterlibraryRequest("IR-1", make_reader(), "Редкая книга", "Нац. библиотека", TODAY)
    librarian = make_librarian()
    request.approve(librarian, TODAY + 5 * DAY)
    assert request.fee == 3.0 and not request.is_overdue(TODAY + 5 * DAY)
    assert request.is_overdue(TODAY + 6 * DAY) and request.days_waiting(TODAY + 2 * DAY) == 2
    request.mark_received()
    assert not request.is_overdue(TODAY + 9 * DAY)
    with pytest.raises(InvalidStatusTransitionError):
        request.approve(librarian, TODAY)


def test_interlibrary_reject():
    request = InterlibraryRequest("IR-2", make_reader(), "Книга", "Библиотека", TODAY)
    request.reject(make_librarian())
    assert request.handled_by is not None
    with pytest.raises(InvalidStatusTransitionError):
        request.mark_received()


def test_subscription_lifecycle():
    magazine = Magazine("IT-5", "Наука", 2026, "0028-1263", 11)
    subscription = Subscription("SB-1", make_reader(), magazine, TODAY, 2)
    assert subscription.is_active_on(TODAY) and subscription.days_left(TODAY) == 60
    subscription.renew(1)
    assert subscription.deliver_issue() == 1 and subscription.days_left(TODAY) == 90
    subscription.cancel()
    assert not subscription.is_active_on(TODAY)
    with pytest.raises(InvalidStatusTransitionError):
        subscription.deliver_issue()
    with pytest.raises(ValidationError):
        Subscription("SB-2", make_reader(), magazine, TODAY, 0)


def test_notification_channels():
    with_email = Notification("NT-1", make_reader(), "Привет", TODAY)
    assert with_email.is_email() and with_email.address() == "ivan@example.by"
    no_email = make_reader()
    no_email.update_email("")
    by_sms = Notification("NT-2", no_email, "Привет", TODAY)
    assert not by_sms.is_email() and by_sms.address() == no_email.phone
    by_sms.mark_read()
    assert by_sms.is_read and by_sms.age_days(TODAY + 3 * DAY) == 3


def test_renewal_and_loan_models_directly():
    reader, copy = make_reader(), make_copy()
    from library_system import Loan, Renewal

    loan = Loan("LN-1", reader, copy, make_librarian(), TODAY, TODAY + 7 * DAY)
    renewal = Renewal("RN-1", loan, TODAY, TODAY + 14 * DAY)
    assert not renewal.is_approved()
    loan.extend(renewal)
    loan.mark_lost()
    with pytest.raises(InvalidStatusTransitionError):
        loan.extend(renewal)
    assert LostItemReport  # модель доступна из пакета


def test_student_gets_longer_period(library):
    student = make_student("RD-0008")
    library.register_reader(student, TODAY)
    library.receive_copy("IT-0001", "BR-0001", 20.0, TODAY)
    loan = library.issue_loan("RD-0008", "CP-0001", "ST-0001", TODAY)
    assert loan.due_on == TODAY + 28 * DAY
