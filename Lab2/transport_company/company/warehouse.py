from datetime import date

from ..exceptions import (
    DeliveryError,
)


class Warehouse:
    """Склад для временного хранения грузов."""

    def __init__(
        self,
        warehouse_id: str,
        name: str,
        address: str,
        capacity_kg: float,
        manager=None,
    ):
        if not warehouse_id or not name or not address:
            raise ValueError("Не заполнены данные склада.")
        if capacity_kg <= 0:
            raise ValueError("Вместимость склада должна быть положительной.")

        self.warehouse_id = warehouse_id
        self.name = name
        self.address = address
        self.capacity_kg = float(capacity_kg)
        self.used_capacity_kg = 0.0
        self.reserved_capacity_kg = 0.0
        self.manager = manager
        self.cargos = {}
        self.is_open = True
        self.opening_date = date.today()
        self.notes = []

    def store_cargo(self, cargo):
        """Размещает груз на складе."""
        cargo_id = getattr(cargo, "cargo_id", None)

        if not self.is_open:
            raise DeliveryError("Склад закрыт.")
        if not cargo_id:
            raise DeliveryError("У груза отсутствует идентификатор.")
        if cargo_id in self.cargos:
            raise DeliveryError("Груз уже находится на складе.")
        if self.get_free_capacity() < cargo.weight_kg:
            raise DeliveryError("Недостаточно свободного места на складе.")

        self.cargos[cargo_id] = cargo
        self.used_capacity_kg += cargo.weight_kg

    def release_cargo(self, cargo_id: str):
        """Выдаёт груз со склада."""
        cargo = self.cargos.get(cargo_id)

        if cargo is None:
            return None

        del self.cargos[cargo_id]
        self.used_capacity_kg = max(
            0.0,
            self.used_capacity_kg - cargo.weight_kg,
        )
        return cargo

    def get_cargo(self, cargo_id: str):
        """Находит груз по идентификатору."""
        return self.cargos.get(cargo_id)

    def find_cargo_by_name(self, name: str):
        """Ищет грузы по названию."""
        search_name = name.lower()

        return [cargo for cargo in self.cargos.values() if search_name in cargo.name.lower()]

    def get_free_capacity(self):
        """Вычисляет свободную вместимость с учётом резерва."""
        return round(
            self.capacity_kg - self.used_capacity_kg - self.reserved_capacity_kg,
            2,
        )

    def reserve_capacity(self, weight_kg: float):
        """Резервирует место для будущего поступления груза."""
        if weight_kg <= 0:
            raise ValueError("Резервируемый вес должен быть положительным.")
        if weight_kg > self.get_free_capacity():
            raise DeliveryError("Недостаточно места для резерва.")

        self.reserved_capacity_kg += weight_kg

    def cancel_reservation(self, weight_kg: float):
        """Снимает резерв вместимости."""
        if weight_kg <= 0 or weight_kg > self.reserved_capacity_kg:
            raise ValueError("Некорректный размер резерва.")

        self.reserved_capacity_kg -= weight_kg

    def calculate_occupancy(self):
        """Вычисляет процент заполненности склада."""
        if self.capacity_kg == 0:
            return 0.0

        return round(
            self.used_capacity_kg / self.capacity_kg * 100,
            2,
        )

    def get_cargo_count(self):
        """Возвращает количество грузов на складе."""
        return len(self.cargos)

    def get_total_cargo_value(self):
        """Считает суммарную объявленную стоимость грузов."""
        return round(
            sum(cargo.declared_value for cargo in self.cargos.values()),
            2,
        )

    def has_cargo(self, cargo_id: str):
        """Проверяет наличие груза на складе."""
        return cargo_id in self.cargos

    def change_manager(self, new_manager):
        """Назначает нового управляющего складом."""
        if new_manager is None:
            raise ValueError("Необходимо указать управляющего.")

        self.manager = new_manager

    def open_warehouse(self):
        """Открывает склад."""
        self.is_open = True

    def close_warehouse(self):
        """Закрывает склад для новых операций."""
        if self.cargos:
            raise DeliveryError("Нельзя закрыть склад, пока на нём остаются грузы.")

        self.is_open = False

    def add_note(self, note: str):
        """Добавляет примечание к складу."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)