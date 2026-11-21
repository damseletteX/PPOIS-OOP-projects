from collections import Counter

from .constants import ID_NUMBER_WIDTH, ID_SEPARATOR
from .enums import IdKind


class IdGenerator:
    """Выдаёт уникальные идентификаторы вида «RD-0001» для каждого типа объектов."""

    def __init__(self):
        self.counters: Counter = Counter()

    def next_id(self, kind: IdKind) -> str:
        """Возвращает следующий идентификатор указанного типа."""
        self.counters[kind] += 1
        number = str(self.counters[kind]).zfill(ID_NUMBER_WIDTH)
        return f"{kind.value}{ID_SEPARATOR}{number}"

    def issued_count(self, kind: IdKind) -> int:
        """Возвращает, сколько идентификаторов типа уже выдано."""
        return self.counters[kind]

    def reset(self, kind: IdKind) -> None:
        """Сбрасывает счётчик для типа объектов."""
        self.counters[kind] = 0
