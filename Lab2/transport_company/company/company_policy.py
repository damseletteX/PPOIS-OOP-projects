from datetime import date, datetime

from ..exceptions import (
    InvalidOrderStatusError,
)


class CompanyPolicy:
    """Правило или внутренний регламент транспортной компании."""

    def __init__(
        self,
        policy_id: str,
        title: str,
        category: str,
        description: str,
        rules: dict | None = None,
        effective_from: date | None = None,
        effective_until: date | None = None,
    ):
        if not policy_id or not title or not category:
            raise ValueError("Не заполнены основные данные правила.")

        self.policy_id = policy_id
        self.title = title
        self.category = category
        self.description = description
        self.rules = dict(rules or {})
        self.effective_from = effective_from or date.today()
        self.effective_until = effective_until
        self.is_enabled = True
        self.applied_count = 0
        self.last_applied_at = None
        self.notes = []

    def set_rule(self, rule_name: str, value):
        """Добавляет новое правило или изменяет существующее."""
        if not self.is_enabled:
            raise ValueError("Нельзя менять отключённое правило.")
        if not rule_name:
            raise ValueError("Название правила не может быть пустым.")

        self.rules[rule_name] = value

    def remove_rule(self, rule_name: str):
        """Удаляет отдельное условие правила."""
        if rule_name not in self.rules:
            return False

        del self.rules[rule_name]
        return True

    def get_rule(self, rule_name: str, default=None):
        """Возвращает значение выбранного условия."""
        return self.rules.get(rule_name, default)

    def is_effective(self, check_date: date | None = None):
        """Проверяет, действует ли правило на выбранную дату."""
        check_date = check_date or date.today()

        if not self.is_enabled:
            return False
        if check_date < self.effective_from:
            return False
        return not (
            self.effective_until is not None and check_date > self.effective_until
        )

    def validate_order(self, order):
        """Проверяет заказ на соответствие внутренним правилам.

        Возвращает список обнаруженных нарушений.
        Пустой список означает, что нарушений не найдено.
        """
        violations = []
        cargos = [item.cargo for item in order.items for _ in range(item.quantity)]

        max_weight = self.get_rule("max_order_weight_kg")
        if max_weight is not None and order.total_weight() > max_weight:
            violations.append("Превышен максимальный вес заказа.")

        max_items = self.get_rule("max_cargo_items")
        if max_items is not None and len(order.items) > max_items:
            violations.append("В заказе слишком много позиций.")

        max_value = self.get_rule("max_order_value")
        if max_value is not None and order.calculate_items_cost() > max_value:
            violations.append("Превышена максимальная стоимость заказа.")

        if self.get_rule("require_packed_cargo", False):  # noqa: SIM102
            if any(not cargo.is_packed for cargo in cargos):
                violations.append("Все грузы должны быть упакованы.")

        if not self.get_rule("allow_dangerous_cargo", True) and any(
            hasattr(cargo, "hazard_class") for cargo in cargos
        ):
            violations.append("Перевозка опасных грузов запрещена правилом.")

        if not self.get_rule("allow_oversized_cargo", True) and any(
            hasattr(cargo, "length_m") for cargo in cargos
        ):
            violations.append("Перевозка негабаритных грузов запрещена правилом.")

        minimum_notice_days = self.get_rule("minimum_notice_days")
        if (
            minimum_notice_days is not None
            and order.requested_delivery_date is not None
        ):
            days_notice = (order.requested_delivery_date - date.today()).days

            if days_notice < minimum_notice_days:
                violations.append("Заказ оформлен слишком близко к дате доставки.")

        return violations

    def check_order(self, order, check_date: date | None = None):
        """Проверяет заказ с учётом срока действия правила."""
        if not self.is_effective(check_date):
            return False

        return not self.validate_order(order)

    def apply_to_order(self, order):
        """Проверяет заказ и регистрирует применение правила."""
        if not self.is_effective():
            raise InvalidOrderStatusError("Правило не действует на текущую дату.")

        violations = self.validate_order(order)

        if violations:
            raise InvalidOrderStatusError(
                "Заказ не соответствует правилам: " + "; ".join(violations)
            )

        self.applied_count += 1
        self.last_applied_at = datetime.now()
        return True

    def enable(self):
        """Включает правило."""
        self.is_enabled = True

    def disable(self):
        """Отключает правило."""
        self.is_enabled = False

    def extend_validity(self, new_date: date):
        """Продлевает срок действия правила."""
        if new_date < self.effective_from:
            raise ValueError("Дата окончания не может быть раньше даты начала.")
        if self.effective_until is not None and new_date < self.effective_until:
            raise ValueError("Продление не должно сокращать срок действия правила.")

        self.effective_until = new_date

    def add_note(self, note: str):
        """Добавляет примечание к правилу."""
        if not note:
            raise ValueError("Примечание не может быть пустым.")

        self.notes.append(note)
