"""Domain classes for the transport company. Standard library only."""
from typing import Optional

class Route:
    """Domain entity: Route. Доменная сущность транспортной компании."""
    def __init__(self, route_code: str, origin: str, destination: str, distance_km: float, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.route_code = route_code
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def calculate_estimated_duration(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Оценивает время в пути по расстоянию и средней скорости.'

    def avoid_restricted_roads(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Исключает запрещённые участки с учётом типа транспорта и разрешений.'

    def recalculate_route(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Пересчитывает длину/время маршрута после изменения дорожных условий.'

class RouteStop:
    """Domain entity: RouteStop. Доменная сущность транспортной компании."""
    def __init__(self, stop_number: int, location: str, planned_arrival: str, stop_type: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.stop_number = stop_number
        self.location = location
        self.planned_arrival = planned_arrival
        self.stop_type = stop_type
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def reschedule_stop(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Меняет плановое время остановки с проверкой последовательности маршрута.'

    def confirm_stop_completion(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Фиксирует фактическое завершение остановки и время выполнения.'

class Trip:
    """Domain entity: Trip. Доменная сущность транспортной компании."""
    def __init__(self, trip_number: str, departure_time: str, arrival_deadline: str, trip_status: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.trip_number = trip_number
        self.departure_time = departure_time
        self.arrival_deadline = arrival_deadline
        self.trip_status = trip_status
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def start_trip(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Переводит рейс в «в пути» только при наличии назначенных ресурсов и проверенного маршрута.'

    def complete_trip(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Закрывает рейс после подтверждения обязательных остановок и статуса доставки.'

    def report_delay(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Регистрирует задержку, причину и обновлённое прогнозное время прибытия.'

class TripAssignment:
    """Domain entity: TripAssignment. Доменная сущность транспортной компании."""
    def __init__(self, assignment_id: str, assigned_at: str, assignment_status: str, dispatcher_id: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.assignment_id = assignment_id
        self.assigned_at = assigned_at
        self.assignment_status = assignment_status
        self.dispatcher_id = dispatcher_id
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def confirm_assignment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Подтверждает назначение при доступности водителя, машины и временного окна.'

    def withdraw_assignment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Снимает назначение и освобождает связанные ресурсы.'

class TollCharge:
    """Domain entity: TollCharge. Доменная сущность транспортной компании."""
    def __init__(self, toll_id: str, road_name: str, charge_amount: float, charged_at: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.toll_id = toll_id
        self.road_name = road_name
        self.charge_amount = charge_amount
        self.charged_at = charged_at
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def allocate_toll_to_trip(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Добавляет дорожный сбор к расходам конкретного рейса.'

    def dispute_toll_charge(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Регистрирует оспаривание сбора с причиной и подтверждающими данными.'

class FuelStop:
    """Domain entity: FuelStop. Доменная сущность транспортной компании."""
    def __init__(self, stop_id: str, fuel_station: str, planned_litres: float, planned_time: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.stop_id = stop_id
        self.fuel_station = fuel_station
        self.planned_litres = planned_litres
        self.planned_time = planned_time
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def confirm_fuel_stop(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Отмечает заправку выполненной и фиксирует фактический объём.'

    def compare_fuel_prices(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Сравнивает плановую цену топлива с альтернативными доступными ценами.'

class Geofence:
    """Domain entity: Geofence. Доменная сущность транспортной компании."""
    def __init__(self, geofence_id: str, center_latitude: float, center_longitude: float, radius_meters: float, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.geofence_id = geofence_id
        self.center_latitude = center_latitude
        self.center_longitude = center_longitude
        self.radius_meters = radius_meters
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def check_vehicle_entry(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет, находится ли координата транспорта внутри геозоны.'

    def trigger_geofence_event(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Создаёт событие входа/выхода при пересечении границы геозоны.'

class TrafficIncident:
    """Domain entity: TrafficIncident. Доменная сущность транспортной компании."""
    def __init__(self, incident_id: str, incident_type: str, reported_at: str, severity: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.incident_id = incident_id
        self.incident_type = incident_type
        self.reported_at = reported_at
        self.severity = severity
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def estimate_delay_impact(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Оценивает задержку по серьёзности инцидента и затронутому участку.'

    def propose_route_detour(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Предлагает объезд, исключающий участок инцидента и соблюдающий ограничения.'

class DeliveryWindow:
    """Domain entity: DeliveryWindow. Доменная сущность транспортной компании."""
    def __init__(self, window_id: str, start_time: str, end_time: str, strictness: str, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.window_id = window_id
        self.start_time = start_time
        self.end_time = end_time
        self.strictness = strictness
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def check_window_feasibility(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет, возможно ли прибыть в пределах интервала доставки.'

    def negotiate_new_window(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Предлагает ближайший реалистичный интервал и фиксирует согласование.'

class TrackingEvent:
    """Domain entity: TrackingEvent. Доменная сущность транспортной компании."""
    def __init__(self, event_id: str, event_type: str, occurred_at: str, latitude: float, trip_id: Optional[str] = None, related_route_id: Optional[str] = None):
        self.event_id = event_id
        self.event_type = event_type
        self.occurred_at = occurred_at
        self.latitude = latitude
        self.trip_id = trip_id
        self.related_route_id = related_route_id

    def record_location_update(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Добавляет координаты и время в историю отслеживания рейса.'

    def notify_customer_of_milestone(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Отправляет клиенту уведомление о ключевом событии доставки.'

