"""Текстовое представление объектов для вывода в консоль."""

from library_system import (
    Fine,
    LibraryEvent,
    LibraryItem,
    Loan,
    Notification,
    PurchaseOrder,
    Reader,
    Staff,
)

from .texts import (
    FORMAT_EVENT,
    FORMAT_FINE,
    FORMAT_ITEM,
    FORMAT_LOAN,
    FORMAT_NOTIFICATION,
    FORMAT_ORDER,
    FORMAT_READER,
    FORMAT_STAFF,
    NO_DATA,
)


def describe_reader(reader: Reader) -> str:
    """Краткое описание читателя."""
    return FORMAT_READER.format(
        reader_id=reader.reader_id,
        name=reader.name,
        plan=reader.membership.plan.value,
        loans=len(reader.active_loans()),
        fines=reader.unpaid_fines_total(),
    )


def describe_item(item: LibraryItem) -> str:
    """Краткое описание издания."""
    return FORMAT_ITEM.format(
        item_id=item.item_id,
        title=item.title,
        authors=item.author_names() or NO_DATA,
        year=item.year,
        available=len(item.available_copies()),
        total=item.copies_count(),
    )


def describe_loan(loan: Loan) -> str:
    """Краткое описание выдачи."""
    return FORMAT_LOAN.format(
        loan_id=loan.loan_id,
        title=loan.copy.item.title,
        reader=loan.reader.name,
        due_on=loan.due_on.isoformat(),
        status=loan.status.value,
    )


def describe_fine(fine: Fine) -> str:
    """Краткое описание штрафа."""
    return FORMAT_FINE.format(
        fine_id=fine.fine_id,
        reason=fine.reason.value,
        amount=fine.amount,
        balance=fine.balance(),
    )


def describe_order(order: PurchaseOrder) -> str:
    """Краткое описание заказа."""
    return FORMAT_ORDER.format(
        order_id=order.order_id,
        supplier=order.supplier.name,
        total=order.total_cost(),
        status=order.status.value,
    )


def describe_event(event: LibraryEvent) -> str:
    """Краткое описание мероприятия."""
    return FORMAT_EVENT.format(
        event_id=event.event_id,
        title=event.title,
        event_date=event.event_date.isoformat(),
        seats=event.seats_left(),
    )


def describe_staff(staff: Staff) -> str:
    """Краткое описание сотрудника."""
    return FORMAT_STAFF.format(
        staff_id=staff.staff_id,
        name=staff.name,
        role=type(staff).__name__,
        salary=staff.salary,
    )


def describe_notification(notification: Notification) -> str:
    """Краткое описание уведомления."""
    return FORMAT_NOTIFICATION.format(
        channel=notification.channel.value,
        address=notification.address(),
        message=notification.message,
    )
