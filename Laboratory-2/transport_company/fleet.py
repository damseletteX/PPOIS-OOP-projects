"""Domain classes for the transport company. Standard library only."""
from typing import Optional

class Vehicle:
    """Domain entity: Vehicle. Доменная сущность транспортной компании."""
    def __init__(self, registration_number: str, make: str, model: str, capacity_kg: float, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.capacity_kg = capacity_kg
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def check_capacity_for_shipment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет массу отправления против грузоподъёмности машины.'

    def mark_out_of_service(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Помечает транспорт недоступным и запрещает назначение на новые рейсы.'

    def record_odometer_reading(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Принимает только неотрицательное показание одометра, не меньше предыдущего.'

class Truck:
    """Domain entity: Truck. Доменная сущность транспортной компании."""
    def __init__(self, trailer_type: str, axle_count: int, fuel_type: str, emissions_class: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.trailer_type = trailer_type
        self.axle_count = axle_count
        self.fuel_type = fuel_type
        self.emissions_class = emissions_class
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def attach_trailer(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет совместимость сцепки и грузоподъёмность, затем фиксирует прицеп.'

    def check_height_restriction(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сравнивает высоту состава с ограничениями маршрута.'

class Van:
    """Domain entity: Van. Доменная сущность транспортной компании."""
    def __init__(self, cargo_volume_m3: float, urban_access_permit: bool, rear_door_height_cm: float, has_refrigeration: bool, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.cargo_volume_m3 = cargo_volume_m3
        self.urban_access_permit = urban_access_permit
        self.rear_door_height_cm = rear_door_height_cm
        self.has_refrigeration = has_refrigeration
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def check_urban_access(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет разрешение на въезд и экологический класс для городской зоны.'

    def optimise_parcel_loading(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Упорядочивает посылки по габаритам/весу с учётом объёма и доступности выгрузки.'

class Trailer:
    """Domain entity: Trailer. Доменная сущность транспортной компании."""
    def __init__(self, trailer_number: str, max_payload_kg: float, trailer_length_m: float, inspection_due: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.trailer_number = trailer_number
        self.max_payload_kg = max_payload_kg
        self.trailer_length_m = trailer_length_m
        self.inspection_due = inspection_due
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def couple_to_vehicle(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет совместимость тягача и прицепа и отсутствие другого активного сцепления.'

    def schedule_trailer_inspection(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Создаёт напоминание об осмотре до даты истечения текущего допуска.'

class RefrigeratedUnit:
    """Domain entity: RefrigeratedUnit. Доменная сущность транспортной компании."""
    def __init__(self, target_temperature: float, current_temperature: float, unit_serial: str, last_calibration: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.target_temperature = target_temperature
        self.current_temperature = current_temperature
        self.unit_serial = unit_serial
        self.last_calibration = last_calibration
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def set_target_temperature(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет допустимый диапазон холодильной установки и задаёт целевую температуру.'

    def raise_temperature_alarm(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Поднимает тревогу, если фактическая температура выходит за допустимые пределы.'

class VehicleInspection:
    """Domain entity: VehicleInspection. Доменная сущность транспортной компании."""
    def __init__(self, inspection_id: str, inspection_date: str, inspector_name: str, result: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.inspection_id = inspection_id
        self.inspection_date = inspection_date
        self.inspector_name = inspector_name
        self.result = result
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def record_defect(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Добавляет дефект к осмотру и отмечает транспорт как требующий проверки/ремонта.'

    def certify_roadworthiness(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Разрешает эксплуатацию только при отсутствии критических дефектов.'

class MaintenanceRecord:
    """Domain entity: MaintenanceRecord. Доменная сущность транспортной компании."""
    def __init__(self, record_id: str, maintenance_type: str, performed_at: str, cost: float, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.record_id = record_id
        self.maintenance_type = maintenance_type
        self.performed_at = performed_at
        self.cost = cost
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def close_maintenance_record(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Закрывает запись обслуживания после фиксации выполненных работ и затрат.'

    def calculate_next_service_date(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Оценивает следующую дату обслуживания по типу работ и регламентному интервалу.'

class FuelTransaction:
    """Domain entity: FuelTransaction. Доменная сущность транспортной компании."""
    def __init__(self, transaction_id: str, litres: float, price_per_litre: float, station_name: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.transaction_id = transaction_id
        self.litres = litres
        self.price_per_litre = price_per_litre
        self.station_name = station_name
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def calculate_fuel_cost(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Возвращает количество литров × цену за литр.'

    def flag_unusual_consumption(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сравнивает расход с нормативом и отмечает аномально высокий расход.'

class Tyre:
    """Domain entity: Tyre. Доменная сущность транспортной компании."""
    def __init__(self, tyre_serial: str, position: str, tread_depth_mm: float, installed_at: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.tyre_serial = tyre_serial
        self.position = position
        self.tread_depth_mm = tread_depth_mm
        self.installed_at = installed_at
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def check_tread_compliance(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сравнивает глубину протектора с минимальным нормативом.'

    def record_tyre_rotation(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Фиксирует перестановку колёс и дату следующей проверки.'

class VehicleDocument:
    """Domain entity: VehicleDocument. Доменная сущность транспортной компании."""
    def __init__(self, document_number: str, document_type: str, valid_until: str, issuing_authority: str, vehicle_id: Optional[str] = None, assigned_employee_id: Optional[str] = None):
        self.document_number = document_number
        self.document_type = document_type
        self.valid_until = valid_until
        self.issuing_authority = issuing_authority
        self.vehicle_id = vehicle_id
        self.assigned_employee_id = assigned_employee_id

    def check_document_validity(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет, что срок действия документа не истёк.'

    def request_document_renewal(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Создаёт заявку на продление документа до даты истечения.'

