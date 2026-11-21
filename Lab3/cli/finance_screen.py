from library_system import PaymentMethod, Supplier
from library_system.enums import IdKind

from .context import AppContext
from .formatters import describe_fine, describe_order
from .menu import Menu, MenuItem
from .texts import (
    FINANCE_ITEMS,
    MENU_FINANCE,
    MSG_BUDGET_SET,
    MSG_NO_FINES,
    MSG_ORDER_APPROVED,
    MSG_ORDER_CREATED,
    MSG_ORDER_RECEIVED,
    MSG_PAYMENT_ACCEPTED,
    MSG_SUPPLIER_ADDED,
    PROMPT_AMOUNT,
    PROMPT_BUDGET_LIMIT,
    PROMPT_BUDGET_YEAR,
    PROMPT_DELIVERY_DAYS,
    PROMPT_FINE_ID,
    PROMPT_NAME,
    PROMPT_ORDER_ID,
    PROMPT_PAYMENT_METHOD,
    PROMPT_PHONE,
    PROMPT_PRICE,
    PROMPT_QUANTITY,
    PROMPT_SUPPLIER_ID,
)


def list_fines(context: AppContext) -> None:
    """Выводит штрафы читателя."""
    reader = context.ask_reader()
    context.io.say_lines(describe_fine(fine) for fine in reader.fines)
    if not reader.fines:
        context.io.say(MSG_NO_FINES)


def pay_fine(context: AppContext) -> None:
    """Принимает оплату штрафа."""
    io = context.io
    reader = context.ask_reader()
    fine_id = io.ask(PROMPT_FINE_ID)
    amount = io.ask_float(PROMPT_AMOUNT)
    method = io.choose_enum(PROMPT_PAYMENT_METHOD, PaymentMethod)
    payment = context.library.pay_fine(reader.reader_id, fine_id, amount, method, context.today)
    io.say(
        MSG_PAYMENT_ACCEPTED.format(payment_id=payment.payment_id, balance=payment.fine.balance())
    )


def set_budget(context: AppContext) -> None:
    """Задаёт бюджет комплектования на год."""
    year = context.io.ask_int(PROMPT_BUDGET_YEAR)
    budget = context.library.set_budget(year, context.io.ask_float(PROMPT_BUDGET_LIMIT))
    context.io.say(MSG_BUDGET_SET.format(year=budget.year, remaining=budget.remaining()))


def add_supplier(context: AppContext) -> None:
    """Регистрирует поставщика."""
    io = context.io
    supplier_id = context.library.ids.next_id(IdKind.SUPPLIER)
    supplier = Supplier(
        supplier_id, io.ask(PROMPT_NAME), io.ask(PROMPT_PHONE), io.ask_int(PROMPT_DELIVERY_DAYS)
    )
    context.library.add_supplier(supplier)
    io.say(MSG_SUPPLIER_ADDED.format(supplier_id=supplier_id))


def create_order(context: AppContext) -> None:
    """Создаёт заказ поставщику с одной позицией."""
    io = context.io
    order = context.library.create_order(io.ask(PROMPT_SUPPLIER_ID), context.today)
    context.library.add_order_line(
        order.order_id,
        context.ask_item_id(),
        io.ask_int(PROMPT_QUANTITY),
        io.ask_float(PROMPT_PRICE),
    )
    io.say(MSG_ORDER_CREATED.format(order_id=order.order_id, total=order.total_cost()))


def approve_order(context: AppContext) -> None:
    """Утверждает заказ директором и отправляет его поставщику."""
    order_id = context.io.ask(PROMPT_ORDER_ID)
    context.library.approve_order(order_id, context.ask_staff_id())
    context.library.send_order(order_id, context.today)
    context.io.say(MSG_ORDER_APPROVED)


def receive_order(context: AppContext) -> None:
    """Принимает поставку и расставляет экземпляры по полкам."""
    order_id = context.io.ask(PROMPT_ORDER_ID)
    branch = context.ask_branch()
    copies = context.library.receive_order(order_id, branch.branch_id, context.today)
    context.io.say(MSG_ORDER_RECEIVED.format(count=len(copies)))


def list_orders(context: AppContext) -> None:
    """Выводит все заказы."""
    context.io.say_lines(describe_order(order) for order in context.library.orders.values())


FINANCE_ACTIONS = (
    list_fines,
    pay_fine,
    set_budget,
    add_supplier,
    create_order,
    approve_order,
    receive_order,
    list_orders,
)


def build_menu() -> Menu:
    """Собирает меню раздела «Финансы и закупки»."""
    items = [MenuItem(label, action) for label, action in zip(FINANCE_ITEMS, FINANCE_ACTIONS)]
    return Menu(MENU_FINANCE, items)
