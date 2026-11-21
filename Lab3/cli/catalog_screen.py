from library_system import Author, Book, LibraryItem, Magazine
from library_system.enums import IdKind

from .context import AppContext
from .formatters import describe_item
from .menu import Menu, MenuItem
from .texts import (
    CATALOG_ITEMS,
    MENU_CATALOG,
    MSG_COPY_ADDED,
    MSG_ITEM_ADDED,
    MSG_NOTHING_FOUND,
    MSG_REVIEW_ADDED,
    PROMPT_AUTHOR_COUNTRY,
    PROMPT_AUTHOR_NAME,
    PROMPT_AUTHOR_YEAR,
    PROMPT_FRAGMENT,
    PROMPT_INDEX_ISBN,
    PROMPT_ISSN,
    PROMPT_ISSUE,
    PROMPT_PAGES,
    PROMPT_PRICE,
    PROMPT_RATING,
    PROMPT_REVIEW_TEXT,
    PROMPT_SEARCH_KIND,
    PROMPT_TITLE,
    PROMPT_YEAR,
    SEARCH_KINDS,
)


def attach_author(context: AppContext, item: LibraryItem) -> None:
    """Привязывает к изданию автора; пустое имя означает «без автора»."""
    io = context.io
    name = io.ask(PROMPT_AUTHOR_NAME)
    if not name:
        return
    author = Author(
        context.library.ids.next_id(IdKind.AUTHOR),
        name,
        io.ask(PROMPT_AUTHOR_COUNTRY),
        io.ask_int(PROMPT_AUTHOR_YEAR),
    )
    context.library.catalog.add_author(author)
    item.add_author(author)


def add_book(context: AppContext) -> None:
    """Добавляет книгу в каталог."""
    io = context.io
    item_id = context.library.ids.next_id(IdKind.ITEM)
    title = io.ask(PROMPT_TITLE)
    year = io.ask_int(PROMPT_YEAR)
    book = Book(item_id, title, year, io.ask(PROMPT_INDEX_ISBN), io.ask_int(PROMPT_PAGES))
    context.library.catalog.add_item(book)
    attach_author(context, book)
    io.say(MSG_ITEM_ADDED.format(item_id=item_id))


def add_magazine(context: AppContext) -> None:
    """Добавляет номер журнала в каталог."""
    io = context.io
    item_id = context.library.ids.next_id(IdKind.ITEM)
    title = io.ask(PROMPT_TITLE)
    year = io.ask_int(PROMPT_YEAR)
    magazine = Magazine(item_id, title, year, io.ask(PROMPT_ISSN), io.ask_int(PROMPT_ISSUE))
    context.library.catalog.add_item(magazine)
    io.say(MSG_ITEM_ADDED.format(item_id=item_id))


def add_copy(context: AppContext) -> None:
    """Принимает новый экземпляр издания в филиал."""
    item_id = context.ask_item_id()
    branch = context.ask_branch()
    price = context.io.ask_float(PROMPT_PRICE)
    copy = context.library.receive_copy(item_id, branch.branch_id, price, context.today)
    context.io.say(MSG_COPY_ADDED.format(number=copy.inventory_number, shelf=copy.shelf.shelf_code))


def search_items(context: AppContext) -> None:
    """Ищет издания по названию или автору."""
    kind = context.io.choose(PROMPT_SEARCH_KIND, SEARCH_KINDS)
    fragment = context.io.ask(PROMPT_FRAGMENT)
    catalog = context.library.catalog
    found = catalog.search_by_title(fragment) if kind == 0 else catalog.search_by_author(fragment)
    context.io.say_lines(describe_item(item) for item in found)
    if not found:
        context.io.say(MSG_NOTHING_FOUND)


def list_items(context: AppContext) -> None:
    """Выводит весь каталог."""
    items = context.library.catalog.items.values()
    context.io.say_lines(describe_item(item) for item in items)


def add_review(context: AppContext) -> None:
    """Сохраняет отзыв читателя."""
    io = context.io
    reader = context.ask_reader()
    item_id = context.ask_item_id()
    rating = io.ask_int(PROMPT_RATING)
    text = io.ask(PROMPT_REVIEW_TEXT)
    context.library.services.add_review(reader.reader_id, item_id, rating, text, context.today)
    io.say(MSG_REVIEW_ADDED)


CATALOG_ACTIONS = (add_book, add_magazine, add_copy, search_items, list_items, add_review)


def build_menu() -> Menu:
    """Собирает меню раздела «Каталог»."""
    items = [MenuItem(label, action) for label, action in zip(CATALOG_ITEMS, CATALOG_ACTIONS)]
    return Menu(MENU_CATALOG, items)
