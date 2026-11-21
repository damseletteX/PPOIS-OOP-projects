"""Перечисления предметной области."""

from enum import Enum


class LoanStatus(Enum):
    ACTIVE = "выдано"
    RETURNED = "возвращено"
    LOST = "утеряно"


class CopyStatus(Enum):
    AVAILABLE = "в наличии"
    LOANED = "на руках"
    RESERVED = "забронировано"
    LOST = "утеряно"
    WRITTEN_OFF = "списано"


class CopyCondition(Enum):
    NEW = "новое"
    GOOD = "хорошее"
    WORN = "потрёпанное"
    DAMAGED = "повреждённое"


class ReservationStatus(Enum):
    ACTIVE = "в очереди"
    READY = "готово к выдаче"
    FULFILLED = "исполнено"
    CANCELLED = "отменено"
    EXPIRED = "истекло"


class PaymentMethod(Enum):
    CASH = "наличные"
    CARD = "карта"
    ONLINE = "онлайн"


class FineReason(Enum):
    OVERDUE = "просрочка"
    DAMAGE = "повреждение"
    LOSS = "утрата"


class OrderStatus(Enum):
    DRAFT = "черновик"
    APPROVED = "утверждён"
    SENT = "отправлен"
    RECEIVED = "получен"
    CANCELLED = "отменён"


class MembershipPlan(Enum):
    BASIC = "базовый"
    STANDARD = "стандартный"
    PREMIUM = "премиум"


class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"


class RequestStatus(Enum):
    REQUESTED = "запрошено"
    APPROVED = "одобрено"
    RECEIVED = "получено"
    REJECTED = "отклонено"


class EbookFormat(Enum):
    PDF = "pdf"
    EPUB = "epub"
    FB2 = "fb2"


class DegreeLevel(Enum):
    BACHELOR = "бакалавр"
    MASTER = "магистр"
    DOCTORAL = "доктор"


class IdKind(Enum):
    """Тип идентификатора; значение — префикс."""

    READER = "RD"
    STAFF = "ST"
    ITEM = "IT"
    COPY = "CP"
    LOAN = "LN"
    RENEWAL = "RN"
    RESERVATION = "RS"
    RETURN = "RT"
    FINE = "FN"
    PAYMENT = "PM"
    ORDER = "PO"
    CARD = "CD"
    NOTIFICATION = "NT"
    REVIEW = "RV"
    BOOKING = "BK"
    EVENT = "EV"
    REGISTRATION = "RG"
    AUTHOR = "AU"
    PUBLISHER = "PB"
    CATEGORY = "CT"
    SHELF = "SH"
    ROOM = "RM"
    BRANCH = "BR"
    SUPPLIER = "SP"
    REPORT = "RP"
    SHIFT = "SF"
    REQUEST = "IR"
    SUBSCRIPTION = "SB"
    AUDIT = "AD"
    DONATION = "DN"
    LIST = "RL"
    BUDGET = "BG"
