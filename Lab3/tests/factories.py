"""Фабрики тестовых объектов с разумными значениями по умолчанию."""

from datetime import date, time

from library_system import (
    Book,
    ChildReader,
    Director,
    ItemCopy,
    Librarian,
    Library,
    Reader,
    StudentReader,
    Supplier,
)

TODAY = date(2026, 11, 21)
ADULT_BIRTH = date(1990, 5, 17)
CHILD_BIRTH = date(2016, 3, 12)
VALID_ISBN = "9780132350884"
PHONE = "+375 29 111-22-33"
OPEN_TIME = time(10, 0)
CLOSE_TIME = time(12, 0)


def make_reader(reader_id: str = "RD-0001", with_card: bool = True) -> Reader:
    """Создаёт обычного читателя, по умолчанию с билетом."""
    reader = Reader(reader_id, "Иван Петров", PHONE, ADULT_BIRTH, TODAY, "ivan@example.by")
    if with_card:
        reader.issue_card("CD-" + reader_id, TODAY)
    return reader


def make_student(reader_id: str = "RD-0002") -> StudentReader:
    """Создаёт студента с билетом."""
    student = StudentReader(reader_id, "Ольга", PHONE, ADULT_BIRTH, TODAY, "S-1", "БГУИР", 3)
    student.issue_card("CD-" + reader_id, TODAY)
    return student


def make_child(guardian: Reader | None = None, consent: bool = True) -> ChildReader:
    """Создаёт ребёнка с билетом и (по умолчанию) согласием опекуна."""
    child = ChildReader(
        "RD-0003", "Миша", PHONE, CHILD_BIRTH, TODAY, guardian or make_reader(), "Школа №5"
    )
    child.issue_card("CD-RD-0003", TODAY)
    if consent:
        child.grant_consent()
    return child


def make_librarian(staff_id: str = "ST-0001") -> Librarian:
    """Создаёт библиотекаря."""
    return Librarian(staff_id, "Анна Лис", PHONE, ADULT_BIRTH, 1500.0, TODAY)


def make_director(staff_id: str = "ST-0009", limit: float = 10000.0) -> Director:
    """Создаёт директора."""
    return Director(staff_id, "Ирина Волкова", PHONE, ADULT_BIRTH, 3000.0, TODAY, limit)


def make_book(item_id: str = "IT-0001", title: str = "Чистый код", age_limit: int = 0) -> Book:
    """Создаёт книгу."""
    return Book(item_id, title, 2008, VALID_ISBN, 464, age_limit=age_limit)


def make_copy(item: Book | None = None, number: str = "CP-0001", price: float = 20.0) -> ItemCopy:
    """Создаёт экземпляр и привязывает его к изданию."""
    book = item or make_book()
    copy = ItemCopy(number, book, price, TODAY)
    book.add_copy(copy)
    return copy


def make_library() -> Library:
    """Создаёт библиотеку с филиалом, персоналом, читателем, книгой и поставщиком."""
    library = Library("Тестовая библиотека", "Минск")
    branch = library.open_branch("Центральный", "ул. Ленина, 1", PHONE)
    library.hire_staff(make_librarian("ST-0001"), branch.branch_id)
    library.hire_staff(make_director("ST-0002"), branch.branch_id)
    library.register_reader(make_reader("RD-0001", with_card=False), TODAY)
    library.catalog.add_item(make_book())
    library.add_supplier(Supplier("SP-0001", "Книготорг", PHONE, 5))
    library.set_budget(TODAY.year, 1000.0)
    return library
