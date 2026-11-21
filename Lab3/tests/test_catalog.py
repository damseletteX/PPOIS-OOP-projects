from datetime import date, timedelta

import pytest

from library_system import (
    AudioBook,
    Author,
    Book,
    Catalog,
    Category,
    CopyCondition,
    CopyStatus,
    DegreeLevel,
    EBook,
    EbookFormat,
    InvalidStatusTransitionError,
    ItemNotAvailableError,
    ItemNotFoundError,
    Magazine,
    Publisher,
    Thesis,
    ValidationError,
)

from .factories import TODAY, VALID_ISBN, make_book, make_child, make_copy, make_reader


def test_author_works_and_life():
    author = Author("AU-1", "Лев Толстой", "Россия", 1828, 1910)
    book = make_book()
    author.add_work(book)
    author.add_work(book)
    assert author.works_count() == 1
    author.remove_work(book)
    author.remove_work(book)
    assert author.works_count() == 0
    assert not author.is_alive() and author.is_contemporary(1900)
    assert not author.is_contemporary(1911) and author.age_at(1900) == 72


def test_living_author_and_invalid_years():
    author = Author("AU-2", "Автор", "США", 1950)
    assert author.is_alive() and author.is_contemporary(2026)
    with pytest.raises(ValidationError):
        Author("AU-3", "Автор", "США", 1950, 1940)


def test_publisher_catalog():
    publisher = Publisher("PB-1", "Питер", "СПб", 1991)
    book = make_book()
    book.set_publisher(publisher)
    publisher.publish(book)
    assert publisher.catalog_size() == 1
    assert publisher.items_published_in(2008) == [book]
    assert publisher.items_published_in(1999) == []
    assert publisher.age_in(2026) == 35


def test_category_tree():
    root = Category("CT-1", "Наука")
    child = Category("CT-2", "Физика", root)
    leaf = Category("CT-3", "Оптика", child)
    book = make_book()
    book.assign_category(leaf)
    assert root.is_root() and not leaf.is_root()
    assert leaf.full_path() == "Наука / Физика / Оптика"
    assert leaf.depth() == 2 and root.depth() == 0
    assert root.includes(leaf) and not leaf.includes(root)
    assert root.all_items() == [book]


def test_review_flow():
    reader = make_reader()
    book = make_book()
    review = reader.write_review("RV-1", book, 4, " ок ", TODAY)
    assert review.is_positive() and review.is_recent(TODAY) and not review.is_approved
    assert book.average_rating() == 0.0
    review.approve()
    assert book.average_rating() == 4.0
    review.edit("плохо", 2)
    assert not review.is_positive() and not review.is_approved
    assert not review.is_recent(TODAY + timedelta(days=100))
    with pytest.raises(ValidationError):
        review.edit("текст", 9)


def test_item_authors_and_copies():
    book = make_book()
    author = Author("AU-1", "Роберт Мартин", "США", 1952)
    book.add_author(author)
    book.add_author(author)
    assert book.author_names() == "Роберт Мартин" and author.works == [book]
    copy = make_copy(book)
    book.add_copy(copy)
    assert book.copies_count() == 1 and book.has_available_copy()
    copy.mark_loaned()
    assert not book.has_available_copy()


def test_item_defaults_and_age():
    book = make_book(age_limit=12)
    assert book.is_loanable() and book.loan_period_days() == 21
    assert book.is_suitable_for_age(12) and not book.is_suitable_for_age(11)
    assert book.is_recent(2010) and not book.is_recent(2026)


def test_copy_loan_return_cycle():
    copy = make_copy()
    assert copy.is_available()
    copy.mark_loaned()
    assert copy.status == CopyStatus.LOANED and copy.loans_count == 1
    copy.mark_returned(CopyCondition.GOOD)
    assert copy.is_available()


def test_copy_reservation_cycle():
    copy = make_copy()
    reader = make_reader()
    copy.mark_reserved(reader)
    assert not copy.is_available() and copy.is_available_for(reader)
    assert not copy.is_available_for(make_reader("RD-0007"))
    copy.release_reservation()
    assert copy.is_available() and copy.reserved_for is None


def test_copy_invalid_transitions():
    copy = make_copy()
    with pytest.raises(InvalidStatusTransitionError):
        copy.mark_returned(CopyCondition.GOOD)
    copy.mark_loaned()
    with pytest.raises(InvalidStatusTransitionError):
        copy.mark_loaned()
    with pytest.raises(InvalidStatusTransitionError):
        copy.write_off()


def test_copy_lost_and_written_off():
    copy = make_copy()
    copy.mark_loaned()
    copy.mark_lost()
    copy.write_off()
    assert copy.status == CopyStatus.WRITTEN_OFF


def test_copy_wear_and_repair():
    copy = make_copy()
    copy.loans_count = 29
    copy.mark_loaned()
    copy.mark_returned(CopyCondition.NEW)
    assert copy.condition == CopyCondition.GOOD
    copy.mark_loaned()
    copy.mark_returned(CopyCondition.DAMAGED)
    assert copy.needs_repair()


def test_book_details():
    book = make_book()
    assert book.reading_time_hours() == 11.6 and not book.is_thick()
    assert book.edition == 1
    book.new_edition()
    assert book.edition == 2
    assert book.citation() == "—. Чистый код. —, 2008."
    book.add_author(Author("AU-1", "Роберт Мартин", "США", 1952))
    book.set_publisher(Publisher("PB-1", "Питер", "СПб", 1991))
    assert book.citation() == "Роберт Мартин. Чистый код. Питер, 2008."


def test_book_rejects_bad_data():
    with pytest.raises(ValidationError):
        Book("IT-2", "Название", 2000, "123", 100)
    with pytest.raises(ValidationError):
        Book("IT-2", "Название", 2000, VALID_ISBN, 0)


def test_magazine_rules():
    magazine = Magazine("IT-5", "Наука", 2026, "0028-1263", 11)
    assert not magazine.is_loanable() and magazine.loan_period_days() == 7
    magazine.archive()
    assert magazine.is_loanable()
    assert magazine.next_issue_number() == 12 and magazine.issue_label() == "№11/2026"


def test_audiobook_details():
    audio = AudioBook("IT-6", "Роман", 2020, "Диктор", 650)
    assert audio.duration_hours() == 10.8 and audio.discs_needed() == 9
    assert audio.is_long() and audio.loan_period_days() == 14
    assert not AudioBook("IT-7", "Рассказ", 2020, "Диктор", 60).is_long()


def test_thesis_rules():
    thesis = Thesis("IT-8", "Диссертация", 2020, "Иванов И.И.", "БГУИР", DegreeLevel.DOCTORAL)
    assert not thesis.is_loanable() and thesis.is_doctoral()
    assert thesis.supervised_by(" иванов и.и. ") and not thesis.supervised_by("Другой")


def test_ebook_download_and_license():
    ebook = EBook("IT-9", "Электронная", 2024, EbookFormat.EPUB, 2.5, TODAY + timedelta(days=5))
    reader = make_reader()
    assert not ebook.is_loanable() and ebook.file_size_bytes() == 2621440
    assert ebook.register_download(reader, TODAY) == 1
    ebook.extend_license(10)
    assert ebook.is_license_valid(TODAY + timedelta(days=15))
    with pytest.raises(ItemNotAvailableError):
        ebook.register_download(reader, TODAY + timedelta(days=30))
    with pytest.raises(ValidationError):
        ebook.extend_license(0)


def test_ebook_age_check():
    ebook = EBook(
        "IT-9", "Для взрослых", 2024, EbookFormat.PDF, 1.0, date(2030, 1, 1), age_limit=18
    )
    with pytest.raises(Exception):
        ebook.register_download(make_child(), TODAY)


def test_catalog_add_get_remove():
    catalog = Catalog()
    book = make_book()
    catalog.add_item(book)
    assert catalog.get_item("IT-0001") is book
    with pytest.raises(ValidationError):
        catalog.add_item(book)
    assert catalog.remove_item("IT-0001") is book
    with pytest.raises(ItemNotFoundError):
        catalog.get_item("IT-0001")


def test_catalog_search():
    catalog = Catalog()
    book = make_book()
    author = Author("AU-1", "Роберт Мартин", "США", 1952)
    book.add_author(author)
    category = Category("CT-1", "ИТ")
    book.assign_category(category)
    other = make_book("IT-0002", "Без рубрики")
    catalog.add_item(book)
    catalog.add_item(other)
    catalog.add_category(category)
    catalog.add_author(author)
    assert catalog.search_by_title("чистый") == [book]
    assert catalog.search_by_author("мартин") == [book]
    assert catalog.search_by_category(category) == [book]
    assert catalog.recent_items(2010) == [book, other]
    assert catalog.available_items() == []


def test_catalog_find_copy():
    catalog = Catalog()
    book = make_book()
    copy = make_copy(book)
    catalog.add_item(book)
    assert catalog.find_copy("CP-0001") is copy
    assert catalog.available_items() == [book]
    with pytest.raises(ItemNotFoundError):
        catalog.find_copy("CP-9999")


def test_base_item_defaults():
    from library_system import LibraryItem

    item = LibraryItem("IT-1", "Издание", 2020)
    assert item.loan_period_days() == 14 and item.language == "русский"
