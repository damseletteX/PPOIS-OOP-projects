from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from ..constants import (
    BYTES_IN_MEGABYTE,
    DEFAULT_LANGUAGE,
    FIELD_DAYS,
    FIELD_QUANTITY,
)
from ..enums import EbookFormat
from ..exceptions import ItemNotAvailableError
from ..validation import require_positive
from .library_item import LibraryItem

if TYPE_CHECKING:
    from ..people.reader import Reader


class EBook(LibraryItem):
    """Электронная книга, доступная по лицензии."""

    def __init__(
        self,
        item_id: str,
        title: str,
        year: int,
        file_format: EbookFormat,
        file_size_mb: float,
        license_until: date,
        language: str = DEFAULT_LANGUAGE,
        age_limit: int = 0,
    ):
        super().__init__(item_id, title, year, language, age_limit)
        self.file_format = file_format
        self.file_size_mb = require_positive(file_size_mb, FIELD_QUANTITY)
        self.license_until = license_until
        self.download_count = 0

    def is_loanable(self) -> bool:
        """Электронные книги не выдаются как физические экземпляры."""
        return False

    def is_license_valid(self, on_date: date) -> bool:
        """Проверяет, действует ли лицензия."""
        return on_date <= self.license_until

    def extend_license(self, days: int) -> None:
        """Продлевает лицензию."""
        require_positive(days, FIELD_DAYS)
        self.license_until += timedelta(days=days)

    def register_download(self, reader: Reader, on_date: date) -> int:
        """Регистрирует скачивание и возвращает общее число скачиваний."""
        reader.ensure_card_valid(on_date)
        reader.ensure_may_read(self, on_date)
        if not self.is_license_valid(on_date):
            raise ItemNotAvailableError(self.title)
        self.download_count += 1
        return self.download_count

    def file_size_bytes(self) -> int:
        """Возвращает размер файла в байтах."""
        return int(self.file_size_mb * BYTES_IN_MEGABYTE)
