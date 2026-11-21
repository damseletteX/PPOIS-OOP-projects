from datetime import date, time, timedelta

import pytest

from library_system import (
    AgeRestrictionError,
    Budget,
    BudgetExceededError,
    CardExpiredError,
    Catalog,
    Cataloger,
    Category,
    MembershipPlan,
    PurchaseLine,
    PurchaseOrder,
    ReaderBlockedError,
    Supplier,
    ValidationError,
)

from .factories import (
    ADULT_BIRTH,
    PHONE,
    TODAY,
    make_book,
    make_child,
    make_director,
    make_librarian,
    make_reader,
    make_student,
)


def test_person_age_before_and_after_birthday():
    reader = make_reader()
    assert reader.age_on(date(2026, 5, 16)) == 35
    assert reader.age_on(date(2026, 5, 17)) == 36
    assert reader.is_adult_on(TODAY)


def test_person_contacts_and_activity():
    reader = make_reader()
    reader.update_phone("+375 44 000-00-00")
    reader.update_email("new@example.by")
    assert "new@example.by" in reader.contact_information()
    reader.deactivate()
    assert not reader.is_active
    reader.activate()
    assert reader.is_active


def test_person_rejects_bad_email():
    with pytest.raises(ValidationError):
        make_reader().update_email("bad")


def test_contact_information_without_email():
    reader = make_reader()
    reader.update_email("")
    assert "—" in reader.contact_information()


def test_membership_limits_and_validity():
    membership = make_reader().membership
    assert membership.loan_limit() == 3
    assert membership.is_valid_on(TODAY)
    assert membership.days_left(TODAY) == 365
    membership.suspend()
    assert not membership.is_valid_on(TODAY)
    membership.resume()
    assert membership.is_valid_on(TODAY)


def test_membership_extend_and_upgrade():
    membership = make_reader().membership
    membership.extend(10)
    assert membership.days_left(TODAY) == 375
    assert membership.upgrade(MembershipPlan.PREMIUM) == 50.0
    assert membership.upgrade(MembershipPlan.BASIC) == 0.0
    with pytest.raises(ValidationError):
        membership.extend(0)


def test_card_lifecycle():
    reader = make_reader()
    card = reader.card
    assert card.is_valid_on(TODAY)
    card.block("утеряна")
    with pytest.raises(ReaderBlockedError):
        card.ensure_usable(TODAY)
    card.unblock()
    card.ensure_usable(TODAY)
    expired_day = card.expires_on + timedelta(days=1)
    with pytest.raises(CardExpiredError):
        card.ensure_usable(expired_day)
    card.renew(expired_day)
    assert card.is_valid_on(expired_day)
    assert card.days_left(TODAY) > 0


def test_reader_card_commands():
    reader = make_reader()
    reader.block_card("причина")
    assert reader.card.is_blocked
    reader.unblock_card()
    assert not reader.card.is_blocked
    assert reader.renew_card(TODAY).expires_on > TODAY


def test_reader_without_card_is_blocked():
    reader = make_reader(with_card=False)
    with pytest.raises(ReaderBlockedError):
        reader.ensure_card_valid(TODAY)
    with pytest.raises(ReaderBlockedError):
        reader.block_card("причина")


def test_inactive_reader_is_blocked():
    reader = make_reader()
    reader.deactivate()
    with pytest.raises(ReaderBlockedError):
        reader.ensure_card_valid(TODAY)


def test_reader_age_restriction():
    reader = make_reader()
    reader.ensure_may_read(make_book(age_limit=16), TODAY)
    child = make_child()
    with pytest.raises(AgeRestrictionError):
        child.ensure_may_read(make_book(age_limit=16), TODAY)


def test_reader_review_and_reading_list():
    reader = make_reader()
    book = make_book()
    review = reader.write_review("RV-1", book, 5, "Отлично", TODAY)
    assert review in book.reviews
    reading_list = reader.create_reading_list("RL-1", "Хочу", TODAY)
    reading_list.add_item(book)
    assert reader.reading_list is reading_list


def test_reader_plan_change_returns_surcharge():
    assert make_reader().change_plan(MembershipPlan.STANDARD) == 20.0


def test_student_limits():
    student = make_student()
    assert student.loan_limit() == 5
    assert student.loan_bonus_days() == 7
    assert make_reader().loan_bonus_days() == 0


def test_student_course_progress():
    student = make_student()
    student.advance_course()
    student.advance_course()
    student.advance_course()
    assert student.course == 6 and student.is_final_year()
    with pytest.raises(ValidationError):
        student.advance_course()
    student.change_university("БГУ")
    assert student.university == "БГУ"


def test_child_limit_and_consent():
    child = make_child(consent=False)
    assert child.loan_limit() == 2
    with pytest.raises(ReaderBlockedError):
        child.ensure_may_read(make_book(), TODAY)
    child.grant_consent()
    child.ensure_may_read(make_book(), TODAY)
    child.revoke_consent()
    assert not child.guardian_consent


def test_child_guardian_rules():
    child = make_child()
    assert child.is_still_child(TODAY)
    child.change_guardian(make_reader("RD-0010"), TODAY)
    with pytest.raises(ValidationError):
        child.change_guardian(make_child(), TODAY)


def test_reading_list_operations():
    reader = make_reader()
    book = make_book()
    reading_list = reader.create_reading_list("RL-1", "Хочу", TODAY)
    reading_list.add_item(book)
    assert reading_list.contains(book) and reading_list.total_items() == 1
    with pytest.raises(ValidationError):
        reading_list.add_item(book)
    assert reading_list.available_items() == []
    reading_list.make_public()
    assert reading_list.is_public
    reading_list.make_private()
    reading_list.remove_item(book)
    assert reading_list.total_items() == 0


def test_staff_salary_and_service():
    librarian = make_librarian()
    librarian.raise_salary(10)
    assert librarian.salary == 1650.0
    assert librarian.annual_salary() == 19800.0
    assert librarian.years_of_service(TODAY + timedelta(days=800)) == 2
    with pytest.raises(ValidationError):
        librarian.raise_salary(80)


def test_staff_shifts():
    from library_system import StaffShift

    librarian = make_librarian()
    first = StaffShift("SF-1", librarian, None, TODAY, time(9, 0), time(13, 0))
    librarian.add_shift(first)
    assert librarian.works_on(TODAY) and not librarian.works_on(TODAY + timedelta(days=1))
    assert librarian.shift_hours_on(TODAY) == 4
    overlapping = StaffShift("SF-2", librarian, None, TODAY, time(12, 0), time(15, 0))
    with pytest.raises(ValidationError):
        librarian.add_shift(overlapping)


def test_librarian_loans_and_languages(library):
    librarian = library.staff.get_librarian("ST-0001")
    assert librarian.issued_count() == 0
    librarian.add_language("Английский")
    librarian.add_language("английский")
    assert librarian.speaks(" английский ") and len(librarian.languages) == 1
    librarian.assign_desk(3)
    assert librarian.desk_number == 3


def test_cataloger_work():
    catalog = Catalog()
    cataloger = Cataloger("ST-0005", "Мария", PHONE, ADULT_BIRTH, 1400.0, TODAY)
    root = Category("CT-1", "Наука")
    child = Category("CT-2", "Физика", root)
    cataloger.set_specialization(root)
    book = make_book()
    cataloger.catalog_item(catalog, book)
    cataloger.classify_item(book, child)
    assert cataloger.cataloged_count() == 1
    assert cataloger.specializes_in(child)
    assert not Cataloger("ST-6", "Пётр", PHONE, ADULT_BIRTH, 1.0, TODAY).specializes_in(child)


def test_director_approval_rules():
    director = make_director(limit=100.0)
    order = PurchaseOrder("PO-1", Supplier("SP-1", "Т", PHONE, 3), TODAY)
    order.add_line(PurchaseLine(make_book(), 2, 30.0))
    budget = Budget("BG-1", TODAY.year, 1000.0)
    assert director.can_approve(order)
    director.approve_order(order, budget)
    assert director.approved_total() == 60.0 and budget.remaining() == 940.0
    director.raise_limit(50.0)
    assert director.approval_limit == 150.0


def test_director_rejects_expensive_order():
    director = make_director(limit=10.0)
    order = PurchaseOrder("PO-1", Supplier("SP-1", "Т", PHONE, 3), TODAY)
    order.add_line(PurchaseLine(make_book(), 2, 30.0))
    with pytest.raises(BudgetExceededError):
        director.approve_order(order, Budget("BG-1", TODAY.year, 1000.0))
    director.reject_order(order)
    assert order.status.value == "отменён"


def test_librarian_issued_on_date(library):
    library.receive_copy("IT-0001", "BR-0001", 20.0, TODAY)
    loan = library.issue_loan("RD-0001", "CP-0001", "ST-0001", TODAY)
    librarian = library.staff.get_librarian("ST-0001")
    assert librarian.issued_on(TODAY) == [loan]
    assert librarian.issued_on(TODAY + timedelta(days=1)) == []
