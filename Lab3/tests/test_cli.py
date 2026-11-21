from datetime import date, time

import pytest

from cli.app import build_main_menu, run
from cli.console_io import ConsoleIO
from cli.context import AppContext
from cli.demo_data import load_demo_data
from cli.menu import Menu, MenuItem
from library_system import CopyCondition, Library, LibraryError, MembershipPlan

from .factories import TODAY

LONG_AGO = date(2026, 10, 1)


class Session:
    """Сценарий работы с консолью: заранее заданный ввод и накопленный вывод."""

    def __init__(self, lines):
        self.answers = iter(lines)
        self.output = []
        self.io = ConsoleIO(self.answer, self.output.append)

    def answer(self, prompt):
        return next(self.answers)

    @property
    def text(self):
        return "\n".join(self.output)


def make_context(lines, with_demo=True, with_old_loan=False, with_fine=False):
    session = Session(lines)
    library = Library("Тест", "Минск")
    if with_demo:
        load_demo_data(library, TODAY)
    if with_old_loan:
        library.issue_loan("RD-0001", "CP-0001", "ST-0002", LONG_AGO)
    if with_fine:
        loan = library.issue_loan("RD-0001", "CP-0001", "ST-0002", LONG_AGO)
        library.return_loan(loan.loan_id, CopyCondition.GOOD, "ST-0002", TODAY)
    return session, AppContext(library, session.io, TODAY)


def play(lines, **options):
    session, context = make_context(lines, **options)
    build_main_menu().run(context)
    return session, context


def test_io_retries_invalid_numbers():
    session = Session(["abc", "7", "x", "2.5"])
    assert session.io.ask_int("n") == 7
    assert session.io.ask_float("f") == 2.5
    assert session.text.count("Введите число") == 2


def test_io_parses_dates_and_times():
    session = Session(["вчера", "2026-11-21", "25:99", "09:30"])
    assert session.io.ask_date("d") == TODAY
    assert session.io.ask_time("t") == time(9, 30)
    assert "формате ГГГГ-ММ-ДД" in session.text and "ЧЧ:ММ" in session.text


def test_io_choose_rejects_out_of_range():
    session = Session(["9", "2"])
    assert session.io.choose("?", ["a", "b"]) == 1
    assert "Нет такого пункта" in session.text


def test_io_choose_enum():
    session = Session(["2"])
    assert session.io.choose_enum("?", MembershipPlan) == MembershipPlan.STANDARD


def test_menu_reports_domain_errors_and_bad_choices():
    def failing_action(context):
        raise LibraryError("сбой")

    session, context = make_context(["abc", "9", "1", "0"], with_demo=False)
    Menu("Тест", [MenuItem("Падает", failing_action)]).run(context)
    assert "Ошибка: сбой" in session.text and "Нет такого пункта" in session.text


def test_run_prints_welcome_and_exits():
    session = Session(["0"])
    run(session.io, TODAY)
    assert "Добро пожаловать" in session.text


def test_load_demo_data():
    session, context = play(["8", "0"], with_demo=False)
    assert "Демонстрационные данные загружены" in session.text
    assert len(context.library.catalog.items) == 5 and len(context.library.readers.readers) == 3


def test_readers_registration_variants():
    lines = ["1", "1", "1", "Тест", "123", "1999-01-01", "t@t.by"]
    lines += ["1", "2", "Студ", "456", "2003-02-02", "", "S-9", "БГУ", "2"]
    lines += ["1", "3", "Дитя", "789", "2017-03-03", "", "RD-0001", "Школа"]
    lines += ["0", "0"]
    session, context = play(lines)
    assert session.text.count("зарегистрирован") == 3
    assert len(context.library.readers.readers) == 6


def test_readers_management():
    lines = ["1", "2", "3", "RD-0001", "4", "RD-0001", "2", "5", "RD-0001", "потерян"]
    lines += ["6", "RD-0001", "7", "RD-0001", "8", "RD-0002", "0", "0"]
    session, context = play(lines)
    assert "тариф: базовый" in session.text and "Тариф изменён на «стандартный»" in session.text
    assert "Билет заблокирован" in session.text and "Билет разблокирован" in session.text
    assert "Билет продлён" in session.text and "RD-0002" not in context.library.readers.readers


def test_readers_error_is_reported():
    session, _ = play(["1", "3", "RD-9999", "0", "0"])
    assert "Ошибка: Читатель «RD-9999» не найден." in session.text


def test_catalog_add_search_and_review():
    lines = ["2", "1", "Новая книга", "2020", "9785960018005", "300", "Автор А", "Беларусь", "1970"]
    lines += ["1", "Без автора", "2021", "9785446101535", "100", ""]
    lines += ["2", "Журнал", "2026", "1234-5678", "3"]
    lines += ["3", "IT-0006", "BR-0001", "12.5"]
    lines += ["4", "1", "война", "4", "2", "автор а", "4", "1", "нет такого"]
    lines += ["5", "6", "RD-0001", "IT-0001", "5", "Отлично", "0", "0"]
    session, context = play(lines)
    assert "Экземпляр CP-0009 поставлен" in session.text and "Ничего не найдено" in session.text
    assert "Отзыв сохранён" in session.text and len(context.library.catalog.items) == 8


def test_catalog_rejects_bad_isbn():
    lines = ["2", "1", "Книга", "2020", "123", "300", "", "0", "0"]
    session, _ = play(lines)
    assert "ISBN" in session.text


def test_circulation_issue_return_with_damage():
    lines = ["3", "1", "RD-0001", "CP-0001", "ST-0002", "2", "LN-0001", "4", "ST-0002", "0", "0"]
    session, context = play(lines)
    assert "Выдача LN-0001 оформлена" in session.text and "начислено штрафов: 1" in session.text
    assert context.library.loan_desk.fines


def test_circulation_return_without_fines_and_renew():
    lines = ["3", "1", "RD-0001", "CP-0001", "ST-0002", "3", "LN-0001", "ST-0002"]
    lines += ["2", "LN-0001", "2", "ST-0002", "0", "0"]
    session, _ = play(lines)
    assert "Срок продлён до" in session.text and "Издание принято." in session.text


def test_circulation_reserve_and_lost():
    lines = ["3", "1", "RD-0001", "CP-0007", "ST-0002", "4", "RD-0002", "IT-0004"]
    lines += ["5", "LN-0001", "0", "0"]
    session, _ = play(lines)
    assert (
        "место в очереди: 1" in session.text
        and "Утрата оформлена, компенсация: 55.00" in session.text
    )


def test_circulation_overdue_lists_and_reminders():
    session, _ = play(["3", "6", "7", "0", "0"], with_old_loan=True)
    assert "LN-0001" in session.text and "Верните" in session.text


def test_circulation_no_overdue_messages():
    session, _ = play(["3", "6", "7", "0", "0"])
    assert session.text.count("Просроченных выдач нет") == 2


def test_finance_without_fines():
    session, _ = play(["4", "1", "RD-0002", "0", "0"])
    assert "Штрафов нет" in session.text


def test_finance_payment_after_late_return():
    lines = ["4", "1", "RD-0001", "2", "RD-0001", "FN-0001", "4.5", "2", "0", "0"]
    session, _ = play(lines, with_fine=True)
    assert "начислено: 14.50" in session.text and "остаток по штрафу: 10.00" in session.text


def test_finance_overpayment_is_rejected():
    lines = ["4", "2", "RD-0001", "FN-0001", "99", "1", "0", "0"]
    session, _ = play(lines, with_fine=True)
    assert "Ошибка: Оплата невозможна" in session.text


def test_finance_purchasing_cycle():
    lines = ["4", "3", "2026", "900", "4", "Новый поставщик", "555", "3"]
    lines += ["5", "SP-0001", "IT-0001", "3", "15", "6", "PO-0001", "ST-0001"]
    lines += ["7", "PO-0001", "BR-0001", "8", "0", "0"]
    session, context = play(lines)
    assert (
        "Бюджет на 2026 год задан" in session.text and "Поставщик добавлен: SP-0002" in session.text
    )
    assert "Заказ PO-0001 создан на сумму 45.00" in session.text
    assert "новых экземпляров: 3" in session.text and "получен" in session.text
    assert len(context.library.orders) == 1


def test_facilities_branches_rooms_and_events():
    lines = ["5", "1", "Филиал 2", "ул. Мира", "555", "2", "3", "BR-0001", "RM-0001", "RD-0001"]
    lines += ["2026-11-21", "10:00", "12:00", "4", "BR-0001", "Лекция", "2026-11-25", "RM-0001"]
    lines += ["ST-0002", "5", "5", "EV-0001", "RD-0001", "6", "0", "0"]
    session, context = play(lines)
    assert "Филиал открыт: BR-0002" in session.text and "Место забронировано" in session.text
    assert "EV-0001 | Лекция" in session.text and "Вы записаны" in session.text
    assert len(context.library.branches) == 2


def test_facilities_interlibrary_and_subscription():
    lines = ["5", "7", "RD-0001", "Редкая книга", "Нац. библиотека", "8", "RD-0001", "IT-0004", "2"]
    lines += ["0", "0"]
    session, _ = play(lines)
    assert "Запрос IR-0001 отправлен" in session.text and "Подписка оформлена до" in session.text


def test_staff_section():
    lines = [
        "6",
        "1",
        "Новый",
        "999",
        "1995-05-05",
        "n@x.by",
        "1200",
        "BR-0001",
        "2",
        "3",
        "0",
        "0",
    ]
    session, _ = play(lines)
    assert (
        "Сотрудник принят: ST-0005" in session.text and "Месячный фонд оплаты труда" in session.text
    )
    assert "Librarian" in session.text


def test_reports_section():
    lines = [
        "7",
        "1",
        "2",
        "2026-10-01",
        "2026-11-21",
        "3",
        "2026-10-01",
        "2026-11-21",
        "3",
        "0",
        "0",
    ]
    session, _ = play(lines, with_old_loan=True)
    assert "Изданий в каталоге: 5" in session.text and "Выдач за период: 1" in session.text
    assert "Популярные издания:" in session.text and "Война и мир: 1" in session.text


def test_library_error_types_are_domain_errors():
    with pytest.raises(LibraryError):
        make_context([], with_demo=False)[1].library.get_branch("BR-1")


def test_empty_reader_list_message():
    session, _ = play(["1", "2", "0", "0"], with_demo=False)
    assert "Читателей пока нет" in session.text
