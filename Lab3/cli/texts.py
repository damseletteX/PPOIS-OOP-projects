"""Тексты консольного интерфейса: меню, подсказки, сообщения и шаблоны вывода."""

# --- Общие ---
EXIT_CHOICE = 0
OPTION_FIRST_NUMBER = 1
EXIT_LABEL = "Назад / выход"
PROMPT_CHOICE = "Выберите пункт: "
OPTION_FORMAT = "  {number}. {option}"
ERROR_PREFIX = "Ошибка: "
ERROR_INVALID_CHOICE = "Нет такого пункта, попробуйте ещё раз."
ERROR_INVALID_NUMBER = "Введите число."
ERROR_INVALID_DATE = "Введите дату в формате ГГГГ-ММ-ДД."
ERROR_INVALID_TIME = "Введите время в формате ЧЧ:ММ."
MSG_WELCOME = "Добро пожаловать в систему управления библиотекой «{name}»!"
MSG_DEMO_LOADED = "Демонстрационные данные загружены: смотрите идентификаторы в списках."
MSG_NOTHING_FOUND = "Ничего не найдено."
NO_DATA = "—"

# --- Главное меню ---
MENU_MAIN = "=== Главное меню ==="
MAIN_ITEMS = (
    "Читатели",
    "Каталог",
    "Выдача и возврат",
    "Финансы и закупки",
    "Филиалы и услуги",
    "Сотрудники",
    "Отчёты",
    "Загрузить демонстрационные данные",
)

# --- Читатели ---
MENU_READERS = "--- Читатели ---"
READERS_ITEMS = (
    "Зарегистрировать читателя",
    "Список читателей",
    "Карточка читателя",
    "Сменить тариф абонемента",
    "Заблокировать билет",
    "Разблокировать билет",
    "Продлить билет",
    "Снять читателя с учёта",
)
READER_KINDS = ("Обычный читатель", "Студент", "Ребёнок")
PROMPT_READER_KIND = "Тип читателя: "
PROMPT_READER_ID = "Идентификатор читателя (например, RD-0001): "
PROMPT_NAME = "Имя: "
PROMPT_PHONE = "Телефон: "
PROMPT_EMAIL = "Email (можно пропустить): "
PROMPT_BIRTH_DATE = "Дата рождения (ГГГГ-ММ-ДД): "
PROMPT_STUDENT_NUMBER = "Номер студенческого: "
PROMPT_UNIVERSITY = "Учебное заведение: "
PROMPT_COURSE = "Курс: "
PROMPT_SCHOOL = "Школа: "
PROMPT_PLAN = "Тариф: "
PROMPT_REASON = "Причина: "
MSG_READER_REGISTERED = "Читатель {reader_id} зарегистрирован, билет {card}."
MSG_NO_READERS = "Читателей пока нет."
MSG_PLAN_CHANGED = "Тариф изменён на «{plan}», доплата: {surcharge:.2f}."
MSG_CARD_BLOCKED = "Билет заблокирован."
MSG_CARD_UNBLOCKED = "Билет разблокирован."
MSG_CARD_RENEWED = "Билет продлён до {expires_on}."
MSG_READER_REMOVED = "Читатель снят с учёта."
TITLE_LOANS = "Выдачи на руках:"
TITLE_FINES = "Штрафы:"
FORMAT_READER = "{reader_id} | {name} | тариф: {plan} | на руках: {loans} | долг: {fines:.2f}"

# --- Каталог ---
MENU_CATALOG = "--- Каталог ---"
CATALOG_ITEMS = (
    "Добавить книгу",
    "Добавить журнал",
    "Принять экземпляр в филиал",
    "Поиск изданий",
    "Весь каталог",
    "Оставить отзыв",
)
SEARCH_KINDS = ("По названию", "По автору")
PROMPT_SEARCH_KIND = "Искать: "
PROMPT_FRAGMENT = "Часть названия или имени: "
PROMPT_ITEM_ID = "Идентификатор издания (например, IT-0001): "
PROMPT_TITLE = "Название: "
PROMPT_YEAR = "Год издания: "
PROMPT_INDEX_ISBN = "ISBN-13: "
PROMPT_PAGES = "Количество страниц: "
PROMPT_ISSN = "ISSN: "
PROMPT_ISSUE = "Номер выпуска: "
PROMPT_AUTHOR_NAME = "Автор (пусто — без автора): "
PROMPT_AUTHOR_COUNTRY = "Страна автора: "
PROMPT_AUTHOR_YEAR = "Год рождения автора: "
PROMPT_PRICE = "Цена экземпляра: "
PROMPT_RATING = "Оценка (1-5): "
PROMPT_REVIEW_TEXT = "Текст отзыва: "
MSG_ITEM_ADDED = "Издание добавлено: {item_id}."
MSG_COPY_ADDED = "Экземпляр {number} поставлен на полку {shelf}."
MSG_REVIEW_ADDED = "Отзыв сохранён и ждёт одобрения."
FORMAT_ITEM = "{item_id} | {title} | {authors} | {year} | в наличии: {available} из {total}"

# --- Выдача и возврат ---
MENU_CIRCULATION = "--- Выдача и возврат ---"
CIRCULATION_ITEMS = (
    "Выдать издание",
    "Принять возврат",
    "Продлить выдачу",
    "Забронировать издание",
    "Оформить утрату",
    "Просроченные выдачи",
    "Разослать напоминания",
)
PROMPT_INVENTORY_NUMBER = "Инвентарный номер экземпляра (например, CP-0001): "
PROMPT_STAFF_ID = "Табельный номер сотрудника (например, ST-0002): "
PROMPT_LOAN_ID = "Номер выдачи (например, LN-0001): "
PROMPT_CONDITION = "Состояние издания: "
MSG_LOAN_ISSUED = "Выдача {loan_id} оформлена, вернуть до {due_on}."
MSG_LOAN_RENEWED = "Срок продлён до {due_on}."
MSG_RETURNED = "Издание принято."
MSG_RETURNED_WITH_FINES = "Издание принято, начислено штрафов: {count}."
MSG_RESERVED = "Бронь оформлена, ваше место в очереди: {position}."
MSG_LOST_REPORTED = "Утрата оформлена, компенсация: {amount:.2f}."
MSG_NO_OVERDUE = "Просроченных выдач нет."
FORMAT_LOAN = "{loan_id} | {title} | {reader} | вернуть до {due_on} | {status}"
FORMAT_NOTIFICATION = "[{channel}] {address}: {message}"

# --- Финансы и закупки ---
MENU_FINANCE = "--- Финансы и закупки ---"
FINANCE_ITEMS = (
    "Штрафы читателя",
    "Оплатить штраф",
    "Задать бюджет",
    "Добавить поставщика",
    "Создать заказ",
    "Утвердить и отправить заказ",
    "Принять поставку",
    "Список заказов",
)
PROMPT_FINE_ID = "Номер штрафа (например, FN-0001): "
PROMPT_AMOUNT = "Сумма: "
PROMPT_PAYMENT_METHOD = "Способ оплаты: "
PROMPT_BUDGET_YEAR = "Год бюджета: "
PROMPT_BUDGET_LIMIT = "Лимит бюджета: "
PROMPT_DELIVERY_DAYS = "Срок доставки, дней: "
PROMPT_SUPPLIER_ID = "Идентификатор поставщика (например, SP-0001): "
PROMPT_QUANTITY = "Количество: "
PROMPT_ORDER_ID = "Номер заказа (например, PO-0001): "
MSG_NO_FINES = "Штрафов нет."
MSG_PAYMENT_ACCEPTED = "Платёж {payment_id} принят, остаток по штрафу: {balance:.2f}."
MSG_BUDGET_SET = "Бюджет на {year} год задан, доступно: {remaining:.2f}."
MSG_SUPPLIER_ADDED = "Поставщик добавлен: {supplier_id}."
MSG_ORDER_CREATED = "Заказ {order_id} создан на сумму {total:.2f}."
MSG_ORDER_APPROVED = "Заказ утверждён и отправлен поставщику."
MSG_ORDER_RECEIVED = "Поставка принята, новых экземпляров: {count}."
FORMAT_FINE = "{fine_id} | {reason} | начислено: {amount:.2f} | остаток: {balance:.2f}"
FORMAT_ORDER = "{order_id} | {supplier} | {total:.2f} | {status}"

# --- Филиалы и услуги ---
MENU_FACILITIES = "--- Филиалы и услуги ---"
FACILITIES_ITEMS = (
    "Открыть филиал",
    "Список филиалов и залов",
    "Забронировать место в зале",
    "Запланировать мероприятие",
    "Записаться на мероприятие",
    "Список мероприятий",
    "Запрос из другой библиотеки (МБА)",
    "Подписка на журнал",
)
PROMPT_BRANCH_ID = "Идентификатор филиала (например, BR-0001): "
PROMPT_ADDRESS = "Адрес: "
PROMPT_ROOM_ID = "Идентификатор зала (например, RM-0001): "
PROMPT_DATE = "Дата (ГГГГ-ММ-ДД): "
PROMPT_START_TIME = "Начало (ЧЧ:ММ): "
PROMPT_END_TIME = "Конец (ЧЧ:ММ): "
PROMPT_MAX_PARTICIPANTS = "Максимум участников: "
PROMPT_EVENT_ID = "Идентификатор мероприятия (например, EV-0001): "
PROMPT_PARTNER = "Библиотека-партнёр: "
PROMPT_MONTHS = "Количество месяцев: "
MSG_BRANCH_OPENED = "Филиал открыт: {branch_id}."
MSG_BOOKED = "Место забронировано ({booking_id}), часов: {hours}."
MSG_EVENT_SCHEDULED = "Мероприятие запланировано: {event_id}."
MSG_EVENT_REGISTERED = "Вы записаны на мероприятие."
MSG_REQUEST_CREATED = "Запрос {request_id} отправлен."
MSG_SUBSCRIBED = "Подписка оформлена до {end_on}."
FORMAT_BRANCH = "{branch_id} | {name} | сотрудников: {staff}"
FORMAT_ROOM = "    зал {room_id} | {name} | мест: {seats}"
FORMAT_EVENT = "{event_id} | {title} | {event_date} | свободных мест: {seats}"

# --- Сотрудники ---
MENU_STAFF = "--- Сотрудники ---"
STAFF_ITEMS = ("Принять библиотекаря", "Список сотрудников", "Фонд оплаты труда")
PROMPT_SALARY = "Оклад: "
MSG_STAFF_HIRED = "Сотрудник принят: {staff_id}."
MSG_PAYROLL = "Месячный фонд оплаты труда: {total:.2f}."
FORMAT_STAFF = "{staff_id} | {name} | {role} | оклад: {salary:.2f}"

# --- Отчёты ---
MENU_REPORTS = "--- Отчёты ---"
REPORTS_ITEMS = ("Сводка по библиотеке", "Отчёт за период", "Популярные издания")
PROMPT_PERIOD_START = "Начало периода (ГГГГ-ММ-ДД): "
PROMPT_PERIOD_END = "Конец периода (ГГГГ-ММ-ДД): "
PROMPT_TOP_LIMIT = "Сколько изданий показать: "
TITLE_POPULAR = "Популярные издания:"
REPORT_LINE = "  {label}: {value}"
