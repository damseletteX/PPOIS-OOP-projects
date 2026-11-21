"""Демонстрационные данные для быстрого знакомства с интерфейсом."""

from datetime import date

from library_system import (
    AudioBook,
    Author,
    Book,
    Cataloger,
    ChildReader,
    Director,
    Librarian,
    Library,
    Magazine,
    Reader,
    StudentReader,
    Supplier,
)
from library_system.enums import IdKind

DEMO_LIBRARY_NAME = "Городская библиотека"
DEMO_LIBRARY_ADDRESS = "г. Минск, ул. Книжная, 1"
DEMO_BRANCH = ("Центральный филиал", "ул. Ленина, 10", "+375 17 200-00-01")
DEMO_BIRTH_DATE = date(1990, 5, 17)
DEMO_STUDENT_BIRTH_DATE = date(2004, 9, 1)
DEMO_CHILD_BIRTH_DATE = date(2016, 3, 12)
DEMO_STAFF_BIRTH_DATE = date(1985, 1, 20)
DEMO_SALARY = 1500.0
DEMO_DIRECTOR_SALARY = 3000.0
DEMO_BOOK_PRICE = 25.0
DEMO_COPIES_PER_BOOK = 2
DEMO_BUDGET_LIMIT = 50000.0
DEMO_SUPPLIER = ("Книготорг", "+375 29 111-22-33", 5)
DEMO_BOOKS = (
    ("Война и мир", 1869, "9785170872367", 1300, "Лев Толстой", "Россия", 1828),
    ("Чистый код", 2008, "9780132350884", 464, "Роберт Мартин", "США", 1952),
    ("Паттерны проектирования", 1994, "9780201633610", 395, "Эрих Гамма", "Швейцария", 1961),
)
DEMO_MAGAZINE = ("Наука и жизнь", 2026, "0028-1263", 11)
DEMO_AUDIOBOOK = ("Мастер и Маргарита", 2020, "Игорь Князев", 960)
DEMO_STAFF_PHONE = "+375 29 000-00-00"
DEMO_STAFF = (
    (Director, "Ирина Волкова", DEMO_DIRECTOR_SALARY),
    (Librarian, "Анна Лис", DEMO_SALARY),
    (Librarian, "Пётр Орлов", DEMO_SALARY),
    (Cataloger, "Мария Кот", DEMO_SALARY),
)
DEMO_REGULAR = ("Сергей Ковалёв", "+375 29 123-45-67", "sergey@example.by")
DEMO_STUDENT = ("Ольга Смирнова", "+375 29 765-43-21", "ST-2026", "БГУИР", 3)
DEMO_CHILD = ("Миша Ковалёв", "Школа №5")


def add_staff(library: Library, on_date: date) -> None:
    """Нанимает директора, двух библиотекарей и каталогизатора."""
    branch_id = next(iter(library.branches))
    for role, name, salary in DEMO_STAFF:
        staff_id = library.ids.next_id(IdKind.STAFF)
        member = role(staff_id, name, DEMO_STAFF_PHONE, DEMO_STAFF_BIRTH_DATE, salary, on_date)
        library.hire_staff(member, branch_id)


def create_regular_reader(library: Library, on_date: date) -> Reader:
    """Создаёт обычного читателя."""
    reader_id = library.ids.next_id(IdKind.READER)
    name, phone, email = DEMO_REGULAR
    return Reader(reader_id, name, phone, DEMO_BIRTH_DATE, on_date, email)


def create_student(library: Library, on_date: date) -> StudentReader:
    """Создаёт читателя-студента."""
    reader_id = library.ids.next_id(IdKind.READER)
    name, phone, student_number, university, course = DEMO_STUDENT
    birth_date = DEMO_STUDENT_BIRTH_DATE
    return StudentReader(
        reader_id, name, phone, birth_date, on_date, student_number, university, course
    )


def create_child(library: Library, on_date: date, guardian: Reader) -> ChildReader:
    """Создаёт читателя-ребёнка с согласием опекуна."""
    reader_id = library.ids.next_id(IdKind.READER)
    name, school = DEMO_CHILD
    birth_date = DEMO_CHILD_BIRTH_DATE
    child = ChildReader(reader_id, name, guardian.phone, birth_date, on_date, guardian, school)
    child.grant_consent()
    return child


def add_readers(library: Library, on_date: date) -> None:
    """Регистрирует обычного читателя, студента и ребёнка."""
    regular = create_regular_reader(library, on_date)
    student = create_student(library, on_date)
    for reader in (regular, student):
        library.register_reader(reader, on_date)
    library.register_reader(create_child(library, on_date, regular), on_date)


def add_books(library: Library, on_date: date) -> None:
    """Добавляет книги, авторов и экземпляры."""
    branch_id = next(iter(library.branches))
    for title, year, isbn, pages, author_name, country, birth_year in DEMO_BOOKS:
        book = Book(library.ids.next_id(IdKind.ITEM), title, year, isbn, pages)
        author = Author(library.ids.next_id(IdKind.AUTHOR), author_name, country, birth_year)
        library.catalog.add_item(book)
        library.catalog.add_author(author)
        book.add_author(author)
        for _ in range(DEMO_COPIES_PER_BOOK):
            library.receive_copy(book.item_id, branch_id, DEMO_BOOK_PRICE, on_date)


def add_periodicals(library: Library, on_date: date) -> None:
    """Добавляет журнал и аудиокнигу."""
    branch_id = next(iter(library.branches))
    title, year, issn, issue = DEMO_MAGAZINE
    magazine = Magazine(library.ids.next_id(IdKind.ITEM), title, year, issn, issue)
    magazine.archive()
    audio_title, audio_year, narrator, minutes = DEMO_AUDIOBOOK
    audiobook = AudioBook(
        library.ids.next_id(IdKind.ITEM), audio_title, audio_year, narrator, minutes
    )
    for item in (magazine, audiobook):
        library.catalog.add_item(item)
        library.receive_copy(item.item_id, branch_id, DEMO_BOOK_PRICE, on_date)


def add_purchasing(library: Library, on_date: date) -> None:
    """Создаёт поставщика и бюджет."""
    name, phone, delivery_days = DEMO_SUPPLIER
    supplier = Supplier(library.ids.next_id(IdKind.SUPPLIER), name, phone, delivery_days)
    library.add_supplier(supplier)
    library.set_budget(on_date.year, DEMO_BUDGET_LIMIT)


def load_demo_data(library: Library, on_date: date) -> None:
    """Наполняет библиотеку демонстрационными данными."""
    library.open_branch(*DEMO_BRANCH)
    add_staff(library, on_date)
    add_readers(library, on_date)
    add_books(library, on_date)
    add_periodicals(library, on_date)
    add_purchasing(library, on_date)
