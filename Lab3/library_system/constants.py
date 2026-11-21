"""Константы предметной области: лимиты, сроки, тарифы и тексты правил."""

from datetime import time

from .enums import CopyCondition, MembershipPlan

# --- Общие ---
ID_NUMBER_WIDTH = 4
ID_SEPARATOR = "-"
CURRENCY_DIGITS = 2
PERCENT_BASE = 100
DAYS_IN_YEAR = 365
DAYS_IN_MONTH = 30
MONTHS_IN_YEAR = 12
MINUTES_IN_HOUR = 60
SECONDS_IN_HOUR = 3600
DEFAULT_LANGUAGE = "русский"
TEXT_JOINER = ", "
PATH_SEPARATOR = " / "

# --- Правила проверки ---
RULE_NOT_EMPTY = "не может быть пустым"
RULE_NON_NEGATIVE = "не может быть отрицательным"
RULE_POSITIVE = "должно быть больше нуля"
RULE_RANGE = "должно быть в диапазоне от {low} до {high}"
RULE_EMAIL = "должно содержать адрес электронной почты"
RULE_ISBN = "содержит некорректный ISBN-13"
RULE_UNIQUE = "должно быть уникальным"
RULE_BEFORE_END = "должно быть раньше даты окончания"
EMAIL_MARKER = "@"
ISBN_SEPARATOR = "-"
ISBN_LENGTH = 13
ISBN_ODD_WEIGHT = 1
ISBN_EVEN_WEIGHT = 3
ISBN_MODULUS = 10

# --- Названия полей для сообщений об ошибках ---
FIELD_NAME = "Имя"
FIELD_PHONE = "Телефон"
FIELD_EMAIL = "Email"
FIELD_ID = "Идентификатор"
FIELD_TITLE = "Название"
FIELD_ISBN = "ISBN"
FIELD_YEAR = "Год"
FIELD_PAGES = "Количество страниц"
FIELD_SALARY = "Зарплата"
FIELD_PRICE = "Цена"
FIELD_AMOUNT = "Сумма"
FIELD_QUANTITY = "Количество"
FIELD_CAPACITY = "Вместимость"
FIELD_RATING = "Оценка"
FIELD_TEXT = "Текст"
FIELD_DAYS = "Количество дней"
FIELD_REASON = "Причина"
FIELD_ADDRESS = "Адрес"
FIELD_PERCENT = "Процент"
FIELD_DATE = "Дата"
FIELD_LIMIT = "Лимит"
FIELD_AGE = "Возраст"
FIELD_COURSE = "Курс"
FIELD_DURATION = "Длительность"
FIELD_TIME = "Время"
FIELD_CODE = "Код"

# --- Люди ---
ADULT_AGE = 18
MIN_COURSE = 1
MAX_COURSE = 6
STUDENT_EXTRA_LOANS = 2
STUDENT_BONUS_DAYS = 7
CHILD_LOAN_LIMIT = 2
CARD_VALIDITY_DAYS = 1095
MAX_SALARY_RAISE_PERCENT = 50
DEFAULT_DESK_NUMBER = 1
DEFAULT_APPROVAL_LIMIT = 10000.0
MEMBERSHIP_FEES = {
    MembershipPlan.BASIC: 0.0,
    MembershipPlan.STANDARD: 20.0,
    MembershipPlan.PREMIUM: 50.0,
}
MEMBERSHIP_LOAN_LIMITS = {
    MembershipPlan.BASIC: 3,
    MembershipPlan.STANDARD: 5,
    MembershipPlan.PREMIUM: 10,
}
REASON_INACTIVE = "читатель неактивен"
REASON_NO_CARD = "нет читательского билета"
REASON_NO_CONSENT = "нет согласия опекуна"
RULE_ADULT = "должно соответствовать совершеннолетнему"
RULE_SHIFT_OVERLAP = "пересекается с другой сменой"

# --- Каталог ---
MIN_RATING = 1
MAX_RATING = 5
POSITIVE_RATING_MIN = 4
RECENT_REVIEW_DAYS = 30
RECENT_ITEM_YEARS = 3
ITEM_LOAN_DAYS = 14
BOOK_LOAN_DAYS = 21
MAGAZINE_LOAN_DAYS = 7
AUDIOBOOK_LOAN_DAYS = 14
PAGES_PER_HOUR = 40
THICK_BOOK_PAGES = 500
AUDIO_DISC_MINUTES = 80
AUDIO_LONG_MINUTES = 600
BYTES_IN_MEGABYTE = 1048576
LOANS_PER_WEAR_STEP = 30
WEAR_PROGRESSION = {
    CopyCondition.NEW: CopyCondition.GOOD,
    CopyCondition.GOOD: CopyCondition.WORN,
}
ITEM_TYPE_COPY = "Экземпляр"
NO_DATA = "—"
RULE_YEAR_ORDER = "года жизни указаны в неверном порядке"

# --- Циркуляция ---
MAX_LOANS_HARD_CAP = 15
MAX_RENEWALS = 2
RENEWAL_DAYS = 7
MAX_UNPAID_FINE = 10.0
RESERVATION_HOLD_DAYS = 3
MAX_QUEUE_LENGTH = 10
INTERLIBRARY_FEE = 3.0
ENTITY_LOAN = "Выдача"
ENTITY_RESERVATION = "Бронь"
ENTITY_SUBSCRIPTION = "Подписка"
ENTITY_REQUEST = "Запрос МБА"
STATE_CANCELLED = "отменена"
ACTION_DELIVERY = "доставка выпуска"
REASON_LOAN_CLOSED = "выдача уже закрыта"
REASON_OVERDUE = "издание просрочено"
REASON_RENEWAL_LIMIT = "исчерпан лимит продлений"
REASON_HAS_QUEUE = "на издание есть очередь"
REASON_AVAILABLE_NOW = "есть свободные экземпляры"
REASON_QUEUE_FULL = "очередь переполнена"
REASON_ALREADY_QUEUED = "читатель уже стоит в очереди"
MESSAGE_RESERVATION_READY = "Издание «{title}» ожидает вас {days} дн."
MESSAGE_OVERDUE_REMINDER = "Верните «{title}»: срок истёк {due_on}."

# --- Финансы ---
FINE_DAILY_RATE = 0.5
FINE_GRACE_DAYS = 1
FINE_MAX_AMOUNT = 50.0
LOSS_PRICE_MULTIPLIER = 2
LOSS_PROCESSING_FEE = 5.0
DONATION_VALUE_RATE = 0.5
RELIABLE_SUPPLIER_RATING = 4.0
DAMAGE_FINE_PERCENT = {CopyCondition.DAMAGED: 50}
ENTITY_ORDER = "Заказ"
REASON_OVERPAYMENT = "сумма превышает остаток по штрафу"
REASON_ALREADY_REFUNDED = "платёж уже возвращён"
REASON_NOT_CASH = "сдача рассчитывается только для наличных"
REASON_TENDER_LOW = "внесённой суммы недостаточно"
RULE_RECEIVE_QUANTITY = "превышает неполученный остаток"

# --- Помещения и расписание ---
DAYS_IN_WEEK = 7
SATURDAY = 5
DEFAULT_OPEN_TIME = time(9, 0)
DEFAULT_CLOSE_TIME = time(18, 0)
DEFAULT_WORKING_WEEKDAYS = frozenset(range(SATURDAY + 1))
REASON_ALREADY_REGISTERED = "читатель уже записан"
REASON_EVENT_CANCELLED = "мероприятие отменено"
RULE_NOT_IN_STAFF = "должно относиться к сотрудникам филиала"

# --- Сервисы и отчёты ---
HISTORY_ENTRY_TEMPLATE = "{date}: {action} — {name}"
LABEL_PERIOD = "Период"
LABEL_LOANS = "Выдач за период"
LABEL_OVERDUE = "Просроченных выдач"
LABEL_AVERAGE_DAYS = "Средняя длительность выдачи, дн."
LABEL_FINES = "Начислено штрафов"
LABEL_COLLECTED = "Получено платежей"
LABEL_ITEMS = "Изданий в каталоге"
LABEL_READERS = "Читателей"
LABEL_STAFF = "Сотрудников"
LABEL_BRANCHES = "Филиалов"
LABEL_LOANS_ACTIVE = "Выдач на руках"
LABEL_FINES_OPEN = "Неоплаченных штрафов"

# --- Филиалы по умолчанию ---
DEFAULT_ROOM_NAME = "Читальный зал"
DEFAULT_ROOM_SEATS = 20
DEFAULT_SHELF_CAPACITY = 100
