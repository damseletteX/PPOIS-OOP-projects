# Система управления библиотекой

Объектная модель предметной области «Библиотека», консольный интерфейс и unit-тесты.
Структура повторяет Lab2: пакет предметной области с подпакетами (один класс — один файл),
`main.py` как точка входа, `tests/`, `pyproject.toml` (uv + hatchling).

## Требования и запуск

Python 3.10+. Внешних зависимостей нет, для разработки нужны `pytest`, `coverage`, `ruff`.

```bash
# окружение (любой из вариантов)
uv sync                                  # или:
python -m pip install -r requirements.txt

python main.py                           # консольное меню
python -m pytest                         # тесты
python -m coverage run -m pytest && python -m coverage report   # покрытие
ruff check . && ruff format --check .    # линтер и форматирование
python tools/check_metrics.py            # проверка количественных и стилевых требований
uv build                                 # сборка (или: python -m pip wheel . --no-deps)
```

В меню пункт **«Загрузить демонстрационные данные»** создаёт филиал, сотрудников, читателей,
книги и экземпляры; идентификаторы (`RD-0001`, `CP-0001`, `ST-0002`…) видны в списках.

## Структура

| Пакет | Содержимое |
|---|---|
| `library_system/people` | Person, Reader, StudentReader, ChildReader, Staff, Librarian, Cataloger, Director, Membership, LibraryCard, ReadingList |
| `library_system/catalog` | LibraryItem → Book, Magazine, AudioBook, Thesis, EBook; ItemCopy, Author, Publisher, Category, Review, Catalog |
| `library_system/circulation` | Loan, LoanDesk, LoanPolicy, Renewal, ReturnRecord, Reservation, WaitingList, InterlibraryRequest, LostItemReport, Subscription, Notification |
| `library_system/finance` | Fine, FinePolicy, Payment, Donation, Budget, Supplier, PurchaseOrder, PurchaseLine |
| `library_system/facilities` | Branch, Shelf, ReadingRoom, SeatBooking, LibraryEvent, EventRegistration, InventoryAudit, StaffShift, OpeningHours |
| `library_system/services` | Library (фасад), ReaderServices, ReaderRegistry, StaffRegistry, LibraryReport |
| `library_system/exceptions` | 19 собственных исключений от `LibraryError` |
| `library_system/constants.py`, `enums.py` | Все числа, тарифы, тексты правил; статусы и типы |
| `cli/` | Консольный интерфейс: меню по разделам, ввод-вывод, демо-данные; не содержит бизнес-логики |
| `tools/check_metrics.py` | Скрипт, который считает классы/поля/поведения/ассоциации и проверяет стиль |

## Соответствие требованиям

Фактические значения (вывод `python tools/check_metrics.py`):

| Требование | Нужно | Есть |
|---|---|---|
| Классы предметной области | ≥ 50 | 57 |
| Поля | ≥ 150 | 309 |
| Уникальные поведения (методы с логикой) | ≥ 100 | 321 |
| Ассоциации (класс как поле или параметр метода) | ≥ 30 | 133 |
| Собственные исключения | ≥ 12 | 19 |
| Покрытие тестами (с учётом `cli`, по веткам) | > 90 % | 99 % |

Стиль: методы ≤ 20 строк, строки ≤ 100 символов (ruff), вложенность ≤ 3, числа и тексты правил
вынесены в `constants.py`, статусы — в `enums.py`, тексты интерфейса — в `cli/texts.py`.
Скрипт проверки не применяет правило «магических чисел» к `tests/`: ожидаемые значения в
проверках записаны литералами.

## Как работает основной сценарий

`Library` (фасад) → `LoanDesk` проверяет билет, возрастное ограничение, лимит выдач, просрочки
и штрафы, выдаёт экземпляр, при возврате начисляет штрафы (`FinePolicy`) и передаёт экземпляр
следующему в очереди (`WaitingList`, `Reservation`, `Notification`). Закупки идут через
`PurchaseOrder` → утверждение директором в пределах `Budget` → поставка → новые `ItemCopy` на полках.
