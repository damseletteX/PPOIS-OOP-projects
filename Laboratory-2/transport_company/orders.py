"""Domain classes for the transport company. Standard library only."""
from typing import Optional

class TransportOrder:
    """Domain entity: TransportOrder. Доменная сущность транспортной компании."""
    def __init__(self, order_number: str, created_at: str, status: str, priority: str, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.order_number = order_number
        self.created_at = created_at
        self.status = status
        self.priority = priority
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def validate_order(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет клиента, состав заказа, приоритет и обязательные данные перед принятием в работу.'

    def cancel_order(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Запрещает отмену уже доставленного/закрытого заказа; иначе меняет статус на «отменён».'

    def change_delivery_window(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет новый временной интервал и отсутствие противоречий с рейсом; обновляет окно доставки.'

class Shipment:
    """Domain entity: Shipment. Доменная сущность транспортной компании."""
    def __init__(self, shipment_number: str, weight_kg: float, volume_m3: float, declared_value: float, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.shipment_number = shipment_number
        self.weight_kg = weight_kg
        self.volume_m3 = volume_m3
        self.declared_value = declared_value
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def split_shipment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Делит отправление на части, проверяя положительные веса/объёмы и сохранение общего количества груза.'

    def consolidate_with_shipment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Объединяет совместимые отправления, если совпадают направление, условия перевозки и требования безопасности.'

class CargoItem:
    """Domain entity: CargoItem. Доменная сущность транспортной компании."""
    def __init__(self, item_code: str, description: str, quantity: int, handling_code: str, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.item_code = item_code
        self.description = description
        self.quantity = quantity
        self.handling_code = handling_code
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def mark_as_fragile(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Добавляет признак хрупкого груза и специальные инструкции по обращению.'

    def calculate_chargeable_weight(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сравнивает фактический и объёмный вес и возвращает больший из них.'

class Package:
    """Domain entity: Package. Доменная сущность транспортной компании."""
    def __init__(self, package_id: str, length_cm: float, width_cm: float, height_cm: float, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.package_id = package_id
        self.length_cm = length_cm
        self.width_cm = width_cm
        self.height_cm = height_cm
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def calculate_volume(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Вычисляет объём упаковки по длине × ширине × высоте с переводом кубических сантиметров в м³.'

    def assign_package_label(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Формирует уникальную этикетку с идентификатором, адресом назначения и штрихкодом/кодом отправления.'

class Pallet:
    """Domain entity: Pallet. Доменная сущность транспортной компании."""
    def __init__(self, pallet_code: str, pallet_type: str, max_load_kg: float, is_returnable: bool, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.pallet_code = pallet_code
        self.pallet_type = pallet_type
        self.max_load_kg = max_load_kg
        self.is_returnable = is_returnable
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def check_load_capacity(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет, что масса груза не превышает допустимую грузоподъёмность паллеты.'

    def register_pallet_return(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Фиксирует возврат многооборотной паллеты и не допускает повторной регистрации.'

class DangerousGoodsDeclaration:
    """Domain entity: DangerousGoodsDeclaration. Доменная сущность транспортной компании."""
    def __init__(self, un_number: str, hazard_class: str, packing_group: str, emergency_contact: str, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.un_number = un_number
        self.hazard_class = hazard_class
        self.packing_group = packing_group
        self.emergency_contact = emergency_contact
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def validate_hazard_documentation(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет UN-номер, класс опасности, группу упаковки и аварийный контакт.'

    def prepare_transport_declaration(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Формирует декларацию опасного груза из проверенных реквизитов.'

class TemperatureRequirement:
    """Domain entity: TemperatureRequirement. Доменная сущность транспортной компании."""
    def __init__(self, minimum_celsius: float, maximum_celsius: float, monitoring_interval_minutes: int, excursion_policy: str, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.minimum_celsius = minimum_celsius
        self.maximum_celsius = maximum_celsius
        self.monitoring_interval_minutes = monitoring_interval_minutes
        self.excursion_policy = excursion_policy
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def check_temperature_reading(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет показание датчика на попадание в допустимый диапазон.'

    def record_temperature_excursion(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Регистрирует выход температуры за пределы и запускает политику реагирования.'

class DeliveryProof:
    """Domain entity: DeliveryProof. Доменная сущность транспортной компании."""
    def __init__(self, proof_number: str, signed_by: str, delivered_at: str, photo_reference: str, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.proof_number = proof_number
        self.signed_by = signed_by
        self.delivered_at = delivered_at
        self.photo_reference = photo_reference
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def verify_recipient_signature(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет наличие подписи получателя и сопоставляет её с данными доставки.'

    def attach_delivery_evidence(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Привязывает фото/подпись/время к подтверждению доставки и сохраняет ссылку на доказательство.'

class ReturnRequest:
    """Domain entity: ReturnRequest. Доменная сущность транспортной компании."""
    def __init__(self, return_number: str, reason: str, requested_at: str, return_status: str, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.return_number = return_number
        self.reason = reason
        self.requested_at = requested_at
        self.return_status = return_status
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def approve_return(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет причину и состояние заказа, после чего одобряет либо отклоняет возврат.'

    def schedule_return_collection(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Создаёт задачу забора возврата с датой, адресом и ответственным рейсом.'

class OrderLine:
    """Domain entity: OrderLine. Доменная сущность транспортной компании."""
    def __init__(self, line_number: int, item_description: str, quantity: int, unit_price: float, customer_id: Optional[str] = None, related_order_id: Optional[str] = None):
        self.line_number = line_number
        self.item_description = item_description
        self.quantity = quantity
        self.unit_price = unit_price
        self.customer_id = customer_id
        self.related_order_id = related_order_id

    def calculate_line_total(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Возвращает количество × цену за единицу; отклоняет отрицательное количество или цену.'

    def change_quantity(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет новое положительное количество и пересчитывает стоимость строки заказа.'

