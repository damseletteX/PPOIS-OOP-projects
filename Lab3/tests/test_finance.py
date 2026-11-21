from datetime import timedelta

import pytest

from library_system import (
    Budget,
    BudgetExceededError,
    CopyCondition,
    Donation,
    Fine,
    FinePolicy,
    FineReason,
    InvalidStatusTransitionError,
    OrderStatus,
    Payment,
    PaymentError,
    PaymentMethod,
    PurchaseLine,
    PurchaseOrder,
    Supplier,
    ValidationError,
)

from .factories import (
    PHONE,
    TODAY,
    make_book,
    make_copy,
    make_director,
    make_librarian,
    make_reader,
)

DAY = timedelta(days=1)


def make_fine(amount=10.0):
    return Fine("FN-1", make_reader(), None, amount, FineReason.OVERDUE, TODAY)


def make_order():
    order = PurchaseOrder("PO-1", Supplier("SP-1", "Книготорг", PHONE, 4), TODAY)
    order.add_line(PurchaseLine(make_book(), 3, 10.0))
    return order


def test_fine_policy_overdue():
    policy = FinePolicy()
    assert policy.is_in_grace_period(1) and not policy.is_in_grace_period(2)
    assert policy.overdue_fine(1) == 0.0 and policy.overdue_fine(5) == 2.0
    assert policy.overdue_fine(1000) == 50.0 and policy.cap(75.0) == 50.0


def test_fine_policy_damage_and_loss():
    policy = FinePolicy()
    assert policy.damage_fine(CopyCondition.DAMAGED, 20.0) == 10.0
    assert policy.damage_fine(CopyCondition.GOOD, 20.0) == 0.0
    assert policy.loss_fine(20.0) == 45.0


def test_fine_payments():
    fine = make_fine()
    payment = Payment("PM-1", fine.reader, fine, 4.0, PaymentMethod.CARD, TODAY)
    payment.process()
    assert fine.balance() == 6.0 and fine.paid_percent() == 40.0 and not fine.is_paid()
    payment.refund()
    assert fine.balance() == 10.0 and payment.is_refunded
    with pytest.raises(PaymentError):
        payment.refund()


def test_fine_rejects_overpayment():
    fine = make_fine()
    with pytest.raises(PaymentError):
        Payment("PM-2", fine.reader, fine, 11.0, PaymentMethod.CASH, TODAY).process()


def test_fine_waive_and_surcharge():
    fine = make_fine()
    fine.add_surcharge(5.0)
    assert fine.amount == 15.0
    fine.waive()
    assert fine.is_paid()
    fine.revert_payment(Payment("PM-3", fine.reader, fine, 1.0, PaymentMethod.CASH, TODAY))
    assert fine.is_paid()


def test_cash_change():
    fine = make_fine()
    cash = Payment("PM-4", fine.reader, fine, 7.5, PaymentMethod.CASH, TODAY)
    assert cash.is_cash() and cash.change_for(10.0) == 2.5
    with pytest.raises(PaymentError):
        cash.change_for(5.0)
    with pytest.raises(PaymentError):
        Payment("PM-5", fine.reader, fine, 1.0, PaymentMethod.CARD, TODAY).change_for(5.0)
    with pytest.raises(ValidationError):
        Payment("PM-6", fine.reader, fine, 0, PaymentMethod.CARD, TODAY)


def test_donation_value():
    donation = Donation("DN-1", make_reader(), TODAY, 10.0)
    donation.add_copy(make_copy(price=20.0))
    donation.accept(make_librarian())
    assert donation.item_count() == 1 and donation.estimated_value() == 20.0
    assert donation.is_monetary() and not donation.is_anonymous()
    assert donation.accepted_by is not None


def test_anonymous_book_donation():
    donation = Donation("DN-2", None, TODAY)
    assert donation.is_anonymous() and not donation.is_monetary()


def test_budget_flow():
    budget = Budget("BG-1", 2026, 100.0)
    budget.reserve(40.0)
    assert budget.remaining() == 60.0 and budget.usage_percent() == 40.0
    with pytest.raises(BudgetExceededError):
        budget.reserve(70.0)
    budget.release(10.0)
    budget.release(1000.0)
    assert budget.spent_amount == 0.0
    budget.reserve(100.0)
    assert budget.is_exhausted()
    budget.increase_limit(50.0)
    assert not budget.is_exhausted()
    order = make_order()
    budget.add_order(order)
    budget.add_order(order)
    assert budget.orders == [order]


def test_supplier_ratings_and_delivery():
    supplier = Supplier("SP-1", "Книготорг", PHONE, 4)
    assert supplier.average_rating() == 0.0 and not supplier.is_reliable()
    supplier.rate(5)
    supplier.rate(4)
    assert supplier.average_rating() == 4.5 and supplier.is_reliable()
    assert supplier.expected_delivery(TODAY) == TODAY + 4 * DAY
    with pytest.raises(ValidationError):
        supplier.rate(6)


def test_supplier_total_ordered():
    order = make_order()
    assert order.supplier.total_ordered() == 30.0


def test_purchase_line_receiving():
    line = PurchaseLine(make_book(), 5, 4.0)
    assert line.total() == 20.0 and line.remaining() == 5
    line.receive(2)
    line.receive(3)
    assert line.is_fully_received()
    with pytest.raises(ValidationError):
        line.receive(1)


def test_order_happy_path():
    order = make_order()
    director = make_director()
    assert order.total_cost() == 30.0 and order.items_count() == 3
    order.mark_approved(director)
    order.send(TODAY)
    assert order.expected_on == TODAY + 4 * DAY and not order.is_overdue(TODAY)
    assert order.is_overdue(TODAY + 10 * DAY)
    line = order.lines[0]
    order.receive_line(line, 1)
    assert order.status == OrderStatus.SENT
    order.receive_line(line, 2)
    assert order.status == OrderStatus.RECEIVED and not order.is_overdue(TODAY + 10 * DAY)


def test_order_invalid_transitions():
    order = make_order()
    with pytest.raises(InvalidStatusTransitionError):
        order.send(TODAY)
    order.cancel()
    with pytest.raises(InvalidStatusTransitionError):
        order.add_line(PurchaseLine(make_book(), 1, 1.0))
    with pytest.raises(InvalidStatusTransitionError):
        order.receive_line(order.lines[0], 1)
