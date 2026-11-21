from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING

from ..catalog.magazine import Magazine
from ..circulation.interlibrary_request import InterlibraryRequest
from ..circulation.subscription import Subscription
from ..enums import IdKind
from ..exceptions import ItemNotFoundError
from ..facilities.inventory_audit import InventoryAudit
from ..facilities.library_event import LibraryEvent
from ..facilities.seat_booking import SeatBooking
from ..finance.donation import Donation

if TYPE_CHECKING:
    from ..catalog.review import Review
    from .library import Library


class ReaderServices:
    """Дополнительные услуги читателям: мероприятия, залы, МБА, подписки, пожертвования."""

    def __init__(self, library: Library):
        self.library = library
        self.events: dict[str, LibraryEvent] = {}
        self.requests: dict[str, InterlibraryRequest] = {}
        self.subscriptions: dict[str, Subscription] = {}
        self.donations: list[Donation] = []
        self.audits: list[InventoryAudit] = []

    def book_seat(
        self,
        branch_id: str,
        room_id: str,
        reader_id: str,
        on_date: date,
        start: time,
        end: time,
    ) -> SeatBooking:
        """Бронирует место в читальном зале."""
        room = self.library.get_branch(branch_id).get_room(room_id)
        reader = self.library.readers.get(reader_id)
        reader.ensure_card_valid(on_date)
        booking_id = self.library.ids.next_id(IdKind.BOOKING)
        return room.book_seat(booking_id, reader, on_date, start, end)

    def schedule_event(
        self,
        title: str,
        event_date: date,
        branch_id: str,
        room_id: str,
        organizer_id: str,
        max_participants: int,
    ) -> LibraryEvent:
        """Планирует мероприятие в читальном зале."""
        room = self.library.get_branch(branch_id).get_room(room_id)
        organizer = self.library.staff.get(organizer_id)
        event_id = self.library.ids.next_id(IdKind.EVENT)
        event = LibraryEvent(event_id, title, event_date, room, organizer, max_participants)
        self.events[event_id] = event
        return event

    def get_event(self, event_id: str) -> LibraryEvent:
        """Возвращает мероприятие по идентификатору."""
        if event_id not in self.events:
            raise ItemNotFoundError(event_id)
        return self.events[event_id]

    def register_for_event(self, event_id: str, reader_id: str, on_date: date):
        """Записывает читателя на мероприятие."""
        event = self.get_event(event_id)
        reader = self.library.readers.get(reader_id)
        registration_id = self.library.ids.next_id(IdKind.REGISTRATION)
        return event.register_reader(registration_id, reader, on_date)

    def request_interlibrary(
        self, reader_id: str, title: str, partner_library: str, on_date: date
    ) -> InterlibraryRequest:
        """Оформляет запрос на издание из другой библиотеки."""
        reader = self.library.readers.get(reader_id)
        request_id = self.library.ids.next_id(IdKind.REQUEST)
        request = InterlibraryRequest(request_id, reader, title, partner_library, on_date)
        self.requests[request_id] = request
        return request

    def approve_request(self, request_id: str, librarian_id: str, expected_on: date) -> None:
        """Одобряет запрос на межбиблиотечный абонемент."""
        if request_id not in self.requests:
            raise ItemNotFoundError(request_id)
        librarian = self.library.staff.get_librarian(librarian_id)
        self.requests[request_id].approve(librarian, expected_on)

    def subscribe(
        self, reader_id: str, magazine_id: str, months: int, on_date: date
    ) -> Subscription:
        """Оформляет подписку на периодическое издание."""
        magazine = self.library.catalog.get_item(magazine_id)
        if not isinstance(magazine, Magazine):
            raise ItemNotFoundError(magazine_id)
        reader = self.library.readers.get(reader_id)
        subscription_id = self.library.ids.next_id(IdKind.SUBSCRIPTION)
        subscription = Subscription(subscription_id, reader, magazine, on_date, months)
        self.subscriptions[subscription_id] = subscription
        return subscription

    def accept_donation(
        self, donor_id: str | None, cash_amount: float, staff_id: str, on_date: date
    ) -> Donation:
        """Принимает денежное пожертвование от читателя или анонимно."""
        donor = self.library.readers.get(donor_id) if donor_id else None
        donation = Donation(self.library.ids.next_id(IdKind.DONATION), donor, on_date, cash_amount)
        donation.accept(self.library.staff.get(staff_id))
        self.donations.append(donation)
        return donation

    def run_inventory(
        self, branch_id: str, auditor_id: str, found_numbers: list[str], on_date: date
    ) -> InventoryAudit:
        """Проводит инвентаризацию филиала по списку найденных инвентарных номеров."""
        branch = self.library.get_branch(branch_id)
        auditor = self.library.staff.get(auditor_id)
        audit = InventoryAudit(self.library.ids.next_id(IdKind.AUDIT), branch, auditor, on_date)
        for number in found_numbers:
            audit.register_found(self.library.catalog.find_copy(number))
        self.audits.append(audit)
        return audit

    def add_review(
        self, reader_id: str, item_id: str, rating: int, text: str, on_date: date
    ) -> Review:
        """Сохраняет отзыв читателя об издании."""
        reader = self.library.readers.get(reader_id)
        item = self.library.catalog.get_item(item_id)
        review_id = self.library.ids.next_id(IdKind.REVIEW)
        return reader.write_review(review_id, item, rating, text, on_date)
