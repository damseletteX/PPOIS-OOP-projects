"""Комплексные unit-тесты модулей транспортной компании."""

from datetime import date, datetime, timedelta

import pytest



from transport_company import (
    # Исключения
    TransportCompanyError,
    InvalidCustomerError,
    InvalidDriverError,
    InvalidVehicleError,
    VehicleUnavailableError,
    DriverUnavailableError,
    InvalidCargoError,
    CargoCapacityExceededError,
    InvalidRouteError,
    InvalidOrderStatusError,
    PaymentError,
    DeliveryError,

    # Люди
    Person,
    Customer,
    CorporateCustomer,
    IndividualCustomer,
    Employee,
    Driver,
    Dispatcher,
    Manager,

    # Транспорт
    Vehicle,
    Truck,
    Van,
    RefrigeratedTruck,
    Tanker,
    FlatbedTruck,
    Trailer,
    VehicleInspection,
    MaintenanceRecord,
    FuelRecord,

    # Грузы
    Cargo,
    PerishableCargo,
    FragileCargo,
    DangerousCargo,
    OversizedCargo,
    CargoPackage,
    CargoDocument,

    # Перевозки
    RoutePoint,
    Route,
    OrderItem,
    TransportOrder,
    Shipment,
    Stop,
    Trip,
    Delivery,
    Schedule,

    # Финансы
    Payment,
    Invoice,
    Transaction,
    Expense,
    Budget,
    SalaryPayment,
    FinancialReport,

    # Управление компанией
    EmployeeRegistry,
    CustomerRegistry,
    OrderRegistry,
    Fleet,
    Warehouse,
    Department,
    Branch,
    CompanyPolicy,
    TransportCompany,
)  # noqa: F401

TODAY = date.today()
FUTURE = TODAY + timedelta(days=30)


def customer(customer_id="C1"):
    obj = IndividualCustomer("Иван Иванов", "+100", "Москва", "ivan@test.ru")
    obj.customer_id = customer_id
    return obj


def driver(employee_id="D1", categories=None):
    return Driver(
        "Пётр",
        "+200",
        employee_id,
        50000,
        "LIC-1",
        categories or ["B", "C"],
        5,
    )


def truck(vehicle_id="V1", available=True):
    obj = Truck(vehicle_id, "Volvo", "FH", 2022, f"REG-{vehicle_id}", 10000, 50)
    obj.is_available = available
    return obj


def cargo(cargo_id="G1", weight=100, volume=2):
    return Cargo(cargo_id, "Груз", weight, volume, 1000)


def order(order_id="O1", client=None, status="new"):
    obj = TransportOrder(order_id, client or customer(), "Москва", "Тверь")
    if status == "pending":
        obj.submit_for_approval()
    elif status == "approved":
        obj.approve()
    elif status == "in_transit":
        obj.approve()
        obj.set_status("in_transit")
    return obj


def route(route_id="R1"):
    return Route(route_id, "Москва-Тверь", "Москва", "Тверь", 180)


def make_trip(trip_id="T1", drv=None, veh=None, rt=None):
    drv = drv or driver()
    veh = veh or truck()
    rt = rt or route()
    if drv.assigned_vehicle is None:
        drv.assign_vehicle(veh)
    return Trip(trip_id, drv, veh, rt, datetime.now())


# ---------------- PEOPLE ----------------


def test_people_and_customers_behaviour_and_validation():
    p = Person(" Анна ", " 123 ", " a@b.ru ")
    assert p.name == "Анна" and p.phone == "123"
    p.update_phone("456")
    p.update_email("new@b.ru")
    assert "456" in p.contact_information()
    p.deactivate()
    assert not p.is_active
    p.activate()
    assert p.is_active
    with pytest.raises(ValueError):
        Person("", "1")
    with pytest.raises(ValueError):
        p.update_phone(" ")

    c = Customer("Клиент", "111", "Адрес")
    c.add_order("order")
    with pytest.raises(ValueError):
        c.add_order("order")
    c.set_discount(10)
    assert c.calculate_discount(200) == 20
    assert c.get_order_count() == 1
    c.verify_customer()
    assert c.is_verified
    c.change_address("Новый адрес")
    c.remove_order("order")
    with pytest.raises(ValueError):
        c.remove_order("missing")
    with pytest.raises(ValueError):
        c.set_discount(101)
    with pytest.raises(ValueError):
        c.calculate_discount(-1)
    c.deactivate()
    with pytest.raises(ValueError):
        c.add_order("blocked")
    with pytest.raises(ValueError):
        c.change_address("")


def test_individual_corporate_employee_driver_dispatcher_manager():
    ic = IndividualCustomer("А", "1", "Адрес")
    with pytest.raises(ValueError):
        ic.set_preferred_contact("email")
    ic.set_preferred_contact("phone")
    with pytest.raises(ValueError):
        ic.set_preferred_contact("fax")
    ic.record_completed_order()
    assert not ic.is_regular_customer()
    for _ in range(4):
        ic.record_completed_order()
    assert ic.is_regular_customer()
    ic.update_passport("P123")
    with pytest.raises(ValueError):
        ic.update_passport(" ")

    cc = CorporateCustomer("ООО", "2", "Адрес", "TAX", "org@test.ru")
    cc.set_contact_person("Мария")
    cc.add_contract("A-1")
    with pytest.raises(ValueError):
        cc.add_contract("A-1")
    cc.set_credit_limit(1000)
    assert cc.can_pay_later(500, 300)
    assert not cc.can_pay_later(900, 300)
    with pytest.raises(ValueError):
        cc.set_credit_limit(-1)
    with pytest.raises(ValueError):
        cc.can_pay_later(-1)

    e = Employee("Сотрудник", "3", "E1", 40000)
    e.assign_task("Отчёт")
    assert not e.is_ready_for_work()
    e.complete_task("Отчёт")
    assert e.is_ready_for_work() and e.calculate_annual_salary() == 480000
    e.change_department("Логистика")
    with pytest.raises(ValueError):
        e.complete_task("x")
    with pytest.raises(ValueError):
        e.assign_task(" ")

    v = truck("V-DRIVER")
    d = driver()
    assert d.can_drive_category("C") and not d.can_drive_category("D")
    d.assign_vehicle(v)
    d.start_trip()
    assert d.is_on_trip and not v.is_available
    d.finish_trip()
    assert d.completed_trips == 1 and d.assigned_vehicle is None
    assert d.is_experienced(3)
    d.update_license_categories(["C"])
    with pytest.raises(ValueError):
        d.update_license_categories([])
    with pytest.raises(ValueError):
        d.finish_trip()

    disp = Dispatcher("Д", "4", "E2", 45000)
    managed_trip = type("TripStub", (), {"trip_id": "trip"})()
    disp.register_trip(managed_trip)
    assert disp.find_managed_trip("missing") is None
    assert disp.find_managed_trip("trip") is managed_trip
    assert disp.has_free_capacity()
    disp.set_shift("night")
    assert disp.shift == "night"
    disp.close_trip(managed_trip)
    with pytest.raises(ValueError):
        disp.set_shift("evening")
    with pytest.raises(ValueError):
        disp.close_trip(managed_trip)

    mgr = Manager("М", "5", "E3", 60000)
    mgr.register_customer(ic)
    mgr.set_monthly_target(1000)
    mgr.record_revenue(250)
    assert mgr.calculate_target_completion() == 25
    mgr.remove_customer(ic)
    with pytest.raises(ValueError):
        mgr.remove_customer(ic)
    with pytest.raises(ValueError):
        mgr.record_revenue(-1)


def test_driver_manager_approval_and_dispatcher_limit():
    d = driver("D2", ["B"])
    wrong_vehicle = Truck("VC", "M", "X", 2020, "R", 100, 5, "C")
    with pytest.raises(ValueError):
        d.assign_vehicle(wrong_vehicle)
    busy = truck("BUSY", False)
    with pytest.raises(ValueError):
        driver("D3").assign_vehicle(busy)

    mgr = Manager("М", "1", "M1", 1)
    o = order("O2")
    mgr.approve_order(o)
    assert o.status == "approved"
    with pytest.raises(ValueError):
        mgr.approve_order(o)
    mgr.deactivate()
    with pytest.raises(ValueError):
        mgr.approve_order(order("O3"))

    disp = Dispatcher("Д", "2", "DP", 1)
    disp.max_trips = 1
    disp.register_trip("T")
    with pytest.raises(ValueError):
        disp.register_trip("T2")


# ---------------- VEHICLES ----------------
def test_vehicle_family_records_and_methods():
    v = Vehicle("V0", "A", "B", 2021, "REG0", 1000)
    assert v.can_transport(500) and not v.can_transport(0)
    v.mark_unavailable()
    assert not v.can_transport(500)
    with pytest.raises(VehicleUnavailableError):
        v.mark_unavailable()
    v.mark_available()
    v.update_mileage(100)
    assert v.calculate_age() >= 0
    with pytest.raises(InvalidVehicleError):
        v.update_mileage(50)
    v.change_location("Тверь")
    with pytest.raises(InvalidVehicleError):
        v.change_location("")
    assert "A B" in str(v)

    t = Truck("V1", "M", "T", 2020, "R1", 5000, 30)
    t.install_crane()
    assert t.has_crane
    t.remove_crane()
    assert not t.has_crane
    assert t.calculate_load_percentage(2500) == 50
    with pytest.raises(InvalidVehicleError):
        t.calculate_load_percentage(6000)

    van = Van("V2", "M", "V", 2020, "R2", 500, 10)
    assert van.open_side_door()
    van.remove_side_door()
    with pytest.raises(InvalidVehicleError):
        van.open_side_door()

    ref = RefrigeratedTruck("V3", "M", "R", 2020, "R3", 5000, 20, -10, 10)
    ref.set_temperature(2)
    ref.enable_cooling()
    assert ref.check_temperature() and ref.cooling_enabled
    ref.disable_cooling()
    with pytest.raises(InvalidVehicleError):
        ref.set_temperature(20)

    tanker = Tanker("V4", "M", "T", 2020, "R4", 5000, 1000)
    tanker.load_liquid(500)
    with pytest.raises(InvalidVehicleError):
        tanker.load_liquid(600)
    with pytest.raises(InvalidVehicleError):
        tanker.clean_tank()
    tanker.unload_liquid(500)
    tanker.mark_tank_dirty()
    with pytest.raises(InvalidVehicleError):
        tanker.load_liquid(10)
    tanker.clean_tank()
    with pytest.raises(InvalidVehicleError):
        tanker.unload_liquid(1)

    flat = FlatbedTruck("V5", "M", "F", 2020, "R5", 5000, 50, 8)
    flat.secure_cargo()
    assert flat.cargo_secured
    flat.release_cargo()
    assert not flat.cargo_secured
    assert flat.can_carry_length(7) and not flat.can_carry_length(9)

    trailer = Trailer("TR", "TR-1", 2000, 10)
    trailer.attach_to(v)
    assert trailer.is_attached and not trailer.is_available
    with pytest.raises(InvalidVehicleError):
        trailer.attach_to(v)
    trailer.detach()
    assert trailer.can_carry(1000)
    with pytest.raises(InvalidVehicleError):
        trailer.detach()


def test_vehicle_inspections_maintenance_fuel_and_associations():
    v1, v2 = truck("V10"), truck("V11")
    inspection = VehicleInspection("I1", v1, TODAY, "Инспектор")
    assert not v1.needs_inspection()
    v1.add_inspection(inspection)
    inspection.conduct(False, "дефект")
    assert not v1.is_available and v1.needs_inspection()
    with pytest.raises(InvalidVehicleError):
        v2.add_inspection(inspection)
    inspection.schedule_next(TODAY + timedelta(days=1))
    assert inspection.is_overdue(TODAY + timedelta(days=2))
    with pytest.raises(InvalidVehicleError):
        inspection.schedule_next(TODAY)

    maintenance = MaintenanceRecord("M1", v1, TODAY, "Ремонт", 100)
    v1.add_maintenance_record(maintenance)
    maintenance.add_part("Фильтр")
    maintenance.update_cost(120)
    maintenance.complete_service()
    assert v1.calculate_total_maintenance_cost() == 120
    with pytest.raises(InvalidVehicleError):
        v2.add_maintenance_record(maintenance)
    with pytest.raises(InvalidVehicleError):
        maintenance.add_part("")
    with pytest.raises(InvalidVehicleError):
        maintenance.update_cost(-1)

    fuel = FuelRecord("F1", v1, TODAY, 20, 2)
    v1.add_fuel_record(fuel)
    assert fuel.calculate_cost() == 40 and v1.calculate_total_fuel() == 20
    fuel.update_price(3)
    assert fuel.total_cost == 60
    with pytest.raises(InvalidVehicleError):
        v2.add_fuel_record(fuel)
    with pytest.raises(InvalidVehicleError):
        fuel.update_price(-1)


# ---------------- CARGO ----------------
def test_cargo_base_packages_documents_and_capacity():
    g = cargo()
    g.set_destination("Москва", "Тверь")
    g.pack()
    assert g.is_packed
    g.unpack()
    g.mark_insured()
    g.update_status("packed")
    assert g.is_packed and g.calculate_density() == 50
    assert "Груз" in str(g)
    assert g.check_vehicle_capacity(truck("CAP"))
    assert not g.check_vehicle_capacity(Truck("LOW", "M", "X", 2020, "L", 10, 1))
    assert not g.check_vehicle_capacity(Tanker("TK", "M", "T", 2020, "TK", 1000, 100))
    with pytest.raises(InvalidCargoError):
        g.set_destination("A", "A")
    with pytest.raises(InvalidCargoError):
        g.update_status("unknown")

    package = CargoPackage("P1", "box", 2, "fragile")
    g.add_package(package)
    with pytest.raises(InvalidCargoError):
        g.add_package(package)
    assert g.calculate_total_packaging_weight() == 2
    package.seal()
    assert package.is_ready_for_transport()
    package.unseal()
    package.mark_damaged("разрыв")
    with pytest.raises(InvalidCargoError):
        package.seal()
    package.replace_label("new label")
    assert not package.is_ready_for_transport()
    with pytest.raises(InvalidCargoError):
        package.replace_label("")

    doc = CargoDocument("DOC1", g, "invoice", TODAY, "Company", FUTURE)
    g.add_document(doc)
    assert g.has_required_documents(["invoice"])
    assert not g.has_required_documents(["permit"])
    doc.verify()
    assert doc.is_verified
    doc.revoke_verification()
    doc.update_number("N-1")
    doc.add_note("note")
    assert not doc.is_expired(FUTURE - timedelta(days=1))
    assert doc.is_expired(FUTURE + timedelta(days=1))
    with pytest.raises(InvalidCargoError):
        g.add_document(doc)
    with pytest.raises(InvalidCargoError):
        g.add_document(CargoDocument("D2", cargo("G2"), "x", TODAY, "Issuer"))
    with pytest.raises(InvalidCargoError):
        doc.update_number("")
    with pytest.raises(InvalidCargoError):
        doc.add_note("")


def test_special_cargo_types():
    perishable = PerishableCargo("P", "Молоко", 10, 1, FUTURE, 4)
    assert not perishable.is_expired(TODAY)
    assert perishable.days_until_expiry(TODAY) == 30
    perishable.record_temperature(4)
    assert perishable.check_storage_temperature(4)
    fridge = RefrigeratedTruck("FR", "M", "R", 2020, "FR", 100, 5, 0, 8)
    fridge.enable_cooling()
    assert perishable.check_refrigerated_vehicle(fridge)
    assert perishable.is_expired(FUTURE + timedelta(days=1))

    fragile = FragileCargo("F", "Стекло", 5, 1, 4)
    fragile.set_handling_instructions("Осторожно")
    assert fragile.assess_damage_risk(2) == "high"
    assert fragile.requires_careful_loading()
    assert FragileCargo("F2", "X", 1, 1, 1).assess_damage_risk(5) == "low"
    assert FragileCargo("F3", "X", 1, 1, 2).assess_damage_risk(3) == "medium"
    with pytest.raises(InvalidCargoError):
        fragile.assess_damage_risk(6)
    with pytest.raises(InvalidCargoError):
        fragile.set_handling_instructions("")

    dangerous = DangerousCargo("D", "Химия", 10, 2, "3", "UN1234")
    assert not dangerous.check_transport_requirements()
    dangerous.set_permit("PERMIT")
    dangerous.set_emergency_contact("112")
    dangerous.add_safety_instruction("Не нагревать")
    assert dangerous.has_valid_permit() and dangerous.check_transport_requirements()
    with pytest.raises(InvalidCargoError):
        dangerous.set_permit("")
    with pytest.raises(InvalidCargoError):
        dangerous.set_emergency_contact("")
    with pytest.raises(InvalidCargoError):
        dangerous.add_safety_instruction("")

    oversized = OversizedCargo("O", "Балка", 100, 10, 6, 2, 1)
    assert oversized.calculate_geometric_volume() == 12
    oversized.set_permit("OS-1")
    oversized.add_route_restriction("Мост")
    oversized.require_escort()
    flat = FlatbedTruck("FL", "M", "F", 2020, "FL", 1000, 20, 8)
    assert oversized.check_flatbed(flat)
    assert not oversized.check_flatbed(truck("NOTFLAT"))
    with pytest.raises(InvalidCargoError):
        oversized.set_permit("")
    with pytest.raises(InvalidCargoError):
        oversized.add_route_restriction("")


# ---------------- TRANSPORT ----------------
def test_routes_points_items_and_order_statuses():
    now = datetime.now()
    point = RoutePoint("P1", "Промежуточная", 1, now)
    assert point.delay_minutes() == 0
    point.record_arrival(now + timedelta(minutes=15))
    assert point.delay_minutes() == 15
    point.set_planned_arrival(now)
    point.add_note("Опоздание")

    r = route()
    p2 = RoutePoint("P2", "Точка 2", 2)
    r.add_point(p2)
    assert r.get_next_point() is p2
    with pytest.raises(InvalidRouteError):
        r.add_point(RoutePoint("P2", "dup", 3))
    with pytest.raises(InvalidRouteError):
        r.add_point(RoutePoint("P3", "dup", 2))
    assert r.calculate_duration(60) == 3
    assert r.calculate_cost(2) == 360
    r.toll_cost = 10
    assert r.calculate_cost(2) == 370
    r.add_restriction("no trucks")
    r.set_active(False)
    assert not r.is_active
    r.set_active(True)
    assert r.progress_percentage() == 0
    p2.record_arrival()
    assert r.progress_percentage() == 100
    assert r.remove_point("P2") and not r.remove_point("X")
    with pytest.raises(InvalidRouteError):
        r.calculate_duration(0)
    with pytest.raises(InvalidRouteError):
        r.calculate_cost(-1)
    with pytest.raises(InvalidRouteError):
        r.add_restriction("")

    g = cargo()
    item = OrderItem("IT1", g, 2)
    item.set_unit_price(50)
    item.set_instructions("Сухо")
    assert item.total_weight() == 200 and item.total_volume() == 4
    assert item.calculate_price() == 100
    item.mark_loaded()
    item.mark_unloaded()
    with pytest.raises(DeliveryError):
        OrderItem("IT2", g).mark_unloaded()

    c = customer()
    o = TransportOrder("O10", c, "Москва", "Тверь")
    o.add_item(item)
    with pytest.raises(InvalidCargoError):
        o.add_item(item)
    assert o.total_weight() == 200 and o.total_volume() == 4
    assert o.calculate_items_cost() == 100
    o.set_route(r)
    o.set_priority("high")
    o.set_delivery_deadline(FUTURE)
    o.submit_for_approval()
    o.approve()
    o.set_status("in_transit")
    o.set_status("delivered")
    assert o.status == "delivered"
    with pytest.raises(InvalidOrderStatusError):
        o.cancel()


def test_shipment_trip_delivery_and_schedule():
    c = customer()
    o = order("O20", c, "pending")
    item = OrderItem("I20", cargo("G20", 100, 1), 1)
    item.cargo.pack()
    item.set_unit_price(25)
    o.add_item(item)
    o.approve()
    sh = Shipment("S1", o)
    assert sh.check_readiness()
    sh.prepare()
    v = truck("VS")
    sh.load_onto(v)
    assert not v.is_available and item.is_loaded
    sh.set_seal_number("SEAL")
    sh.unload()
    assert item.is_unloaded and sh.unloading_time is not None

    d = driver("DT")
    veh = truck("VT")
    d.assign_vehicle(veh)
    rt = route("RT")
    trip = Trip("TRIP", d, veh, rt, datetime.now() - timedelta(hours=2))
    o2 = order("O21", customer(), "approved")
    trip.add_order(o2)
    trip.add_stop(Stop("ST", "Кафе", "rest"))
    trip.start()
    assert trip.status == "in_progress" and o2.status == "in_transit"
    trip.finish()
    assert trip.status == "completed" and o2.status == "delivered"
    assert trip.calculate_duration_hours() >= 0
    assert trip.calculate_average_speed() >= 0

    # cancellation route and planned trip removal
    d2 = driver("DT2")
    v2 = truck("VT2")
    d2.assign_vehicle(v2)
    trip2 = Trip("TRIP2", d2, v2, rt, datetime.now() + timedelta(days=1))
    trip2.cancel("тест")
    assert trip2.status == "cancelled"
    schedule = Schedule("SCH", "Основное")
    d3 = driver("DT3")
    v3 = truck("VT3")
    d3.assign_vehicle(v3)
    trip3 = Trip("TRIP3", d3, v3, rt, datetime.now() + timedelta(days=2))
    schedule.add_trip(trip3)
    assert trip3 in schedule.get_available_trips()
    assert schedule.get_trips_for_date(trip3.departure_time.date()) == [trip3]
    with pytest.raises(InvalidRouteError):
        schedule.add_trip(trip3)
    assert schedule.remove_trip("TRIP3")
    assert not schedule.remove_trip("missing")
    schedule.add_trip(trip3)
    schedule.add_note("Примечание")
    schedule.cancel_schedule()
    assert trip3.status == "cancelled"

    delivery_order = order("O22", customer(), "in_transit")
    delivery = Delivery("DEL", delivery_order, "Получатель", "Адрес", TODAY)
    assert delivery.is_late(TODAY + timedelta(days=1))
    delivery.mark_in_transit()
    delivery.record_recipient("Новый получатель")
    delivery.confirm_delivery("Новый получатель", "подпись")
    assert delivery.status == "delivered" and delivery_order.status == "delivered"
    assert not delivery.is_late(TODAY + timedelta(days=10))

    fail_delivery = Delivery("DEL2", order("O23"), "Получатель", "Адрес", TODAY)
    fail_delivery.report_failure("Адрес не найден")
    fail_delivery.reschedule(FUTURE)
    assert fail_delivery.status == "scheduled"


def test_transport_error_branches_and_stop_methods():
    st = Stop("STOP", "Адрес", "loading")
    st.schedule(datetime.now())
    st.complete(datetime.now() + timedelta(minutes=5))
    assert st.delay_minutes() == 5
    st.add_note("Ожидание")

    p = RoutePoint("RP", "A", 1)
    with pytest.raises(InvalidRouteError):
        p.add_note("")
    with pytest.raises(InvalidRouteError):
        RoutePoint("", "A", 0)
    with pytest.raises(InvalidRouteError):
        Route("X", "x", "A", "A", 2)
    with pytest.raises(InvalidRouteError):
        Route("X", "x", "A", "B", 0)
    with pytest.raises(InvalidRouteError):
        TransportOrder("x", customer(), "A", "A")

    o = order("ERR")
    with pytest.raises(InvalidOrderStatusError):
        o.set_status("delivered")
    with pytest.raises(InvalidOrderStatusError):
        o.set_priority("strange")
    with pytest.raises(InvalidOrderStatusError):
        o.set_delivery_deadline(TODAY - timedelta(days=1))
    o.cancel()
    with pytest.raises(InvalidOrderStatusError):
        o.add_item(OrderItem("x", cargo()))

    empty_order = order("EMPTY", status="approved")
    empty_shipment = Shipment("EMPTY-S", empty_order)
    assert not empty_shipment.check_readiness()
    with pytest.raises(DeliveryError):
        empty_shipment.prepare()

    o_fail = order("DLFAIL")
    dl = Delivery("DF", o_fail, "R", "A", TODAY)
    with pytest.raises(DeliveryError):
        dl.confirm_delivery("R")
    with pytest.raises(DeliveryError):
        dl.report_failure("")
    dl.report_failure("no answer")
    with pytest.raises(DeliveryError):
        dl.reschedule(TODAY - timedelta(days=1))

    rt = route()
    d = driver("DU")
    v = truck("VU")
    d.assign_vehicle(v)
    planned = Trip("P-TRIP", d, v, rt, datetime.now())
    with pytest.raises(InvalidOrderStatusError):
        planned.finish()
    planned.add_note("note")
    with pytest.raises(InvalidRouteError):
        planned.add_note("")
    another_driver = driver("DU2")
    bad_trip = Trip("BAD", another_driver, truck("BADV"), rt, datetime.now())
    with pytest.raises(DriverUnavailableError):
        bad_trip.start()

    inactive = Schedule("S2", "inactive")
    inactive.is_active = False
    with pytest.raises(InvalidRouteError):
        inactive.add_trip(planned)
    with pytest.raises(InvalidRouteError):
        inactive.add_note("")


# ---------------- FINANCE ----------------
def test_payment_invoice_transaction_lifecycle():
    o = order("FIN")
    it = OrderItem("FI", cargo("FG"))
    it.set_unit_price(100)
    o.add_item(it)
    inv = Invoice("INV", o, FUTURE, tax_rate=0.2)
    inv.add_charge("Услуга", 10)
    inv.apply_discount(5)
    assert inv.calculate_subtotal() == 100
    assert inv.calculate_tax() == 21
    assert inv.calculate_total() == 126
    inv.issue()
    assert inv.can_accept_payment(50)
    p1 = Payment("PAY1", o, 50, "card", inv)
    p1.change_payment_method("transfer")
    tx = p1.process()
    assert tx.status == "successful" and inv.amount_paid == 50
    with pytest.raises(PaymentError):
        p1.process()
    assert p1.is_successful()
    p1.refund(10)
    assert inv.amount_paid == 40 and p1.remaining_refundable_amount() == 40
    p1.refund()
    assert p1.status == "refunded"

    tx2 = Transaction("TX2", p1, "payment", 3)
    tx2.set_external_reference("BANK-1")
    tx2.mark_successful()
    tx2.reverse("дубль")
    assert tx2.status == "reversed"
    tx3 = Transaction("TX3", p1, "refund", 1)
    tx3.mark_failed("declined")
    assert tx3.is_refund() and tx3.failure_reason == "declined"

    failed = Payment("FAIL", o, 5, "cash")
    failed.fail("отказ")
    assert failed.status == "failed"
    with pytest.raises(PaymentError):
        failed.refund()


def test_finance_expenses_budget_salary_report():
    manager = Manager("Boss", "1", "B1", 1000)
    expense = Expense("E1", "fuel", "Топливо", 100, TODAY, "RC-1")
    assert expense.has_receipt()
    expense.update_amount(120)
    expense.change_category("fueling")
    expense.add_note("note")
    expense.approve(manager)
    expense.mark_reimbursed()
    assert expense.status == "reimbursed"

    pending = Expense("E2", "fuel", "Ремонт", 50, TODAY)
    pending.reject("не согласовано")
    assert pending.status == "rejected"

    budget_exp = Expense("E3", "fuel", "Бензин", 120, TODAY)
    budget_exp.approve(manager)
    budget = Budget("BUD", "fuel", 100, TODAY - timedelta(days=1), FUTURE)
    budget.add_expense(budget_exp)
    assert budget.calculate_spent() == 120
    assert budget.calculate_remaining() == -20 and budget.is_exceeded()
    assert budget.get_usage_percentage() == 120
    assert budget.remove_expense("E3")
    assert not budget.remove_expense("missing")
    zero_budget = Budget("B0", "other", 0, TODAY, FUTURE)
    assert zero_budget.get_usage_percentage() == 0
    budget.close()
    budget.reopen()
    budget.change_limit(200)
    budget.add_note("n")

    employee = Employee("Worker", "1", "W1", 2000)
    salary = SalaryPayment("SAL", employee, TODAY - timedelta(days=1), FUTURE, 2000)
    salary.add_bonus(200)
    salary.add_deduction(100)
    assert salary.calculate_net_amount() == 2100
    salary.pay(TODAY)
    assert salary.is_paid()

    o = order("REPORT")
    payment = Payment("P-REPORT", o, 300, "cash", payment_date=TODAY)
    payment.status = "completed"
    report_exp = Expense("RE", "fuel", "expense", 120, TODAY)
    report_exp.approve(manager)
    report = FinancialReport("REP", TODAY - timedelta(days=1), FUTURE)
    report.add_payment(payment)
    report.add_expense(report_exp)
    report.add_salary_payment(salary)
    assert report.calculate_revenue() == 300
    assert report.calculate_expenses() == 120
    assert report.calculate_salary_costs() == 2100
    assert report.calculate_profit() == -1920
    assert report.get_payment_count() == 1
    summary = report.generate_summary()
    assert summary["report_id"] == "REP"
    report.add_note("final note")
    report.finalize()


def test_finance_validation_paths():
    o = order("FERR")
    it = OrderItem("FE", cargo("FEC"))
    it.set_unit_price(10)
    o.add_item(it)
    inv = Invoice("INVERR", o, FUTURE)
    with pytest.raises(ValueError):
        inv.add_charge("", 1)
    with pytest.raises(ValueError):
        inv.apply_discount(100)
    inv.cancel()
    assert inv.status == "cancelled"
    inv.status = "paid"
    with pytest.raises(PaymentError):
        inv.cancel()

    bad_payment = Payment("BAD-P", o, 1, "cash", inv)
    with pytest.raises(PaymentError):
        bad_payment.process()  # счёт не выставлен
    bad_payment.change_payment_method("card")
    bad_payment.status = "completed"
    with pytest.raises(PaymentError):
        bad_payment.change_payment_method("wire")

    exp = Expense("X", "cat", "desc", 5, TODAY)
    with pytest.raises(ValueError):
        exp.approve(None)
    with pytest.raises(ValueError):
        exp.update_amount(0)
    with pytest.raises(ValueError):
        exp.change_category("")
    with pytest.raises(ValueError):
        exp.add_note("")

    budget = Budget("BB", "cat", 10, TODAY, FUTURE)
    with pytest.raises(ValueError):
        budget.add_expense(Expense("OUT", "other", "d", 1, TODAY))
    budget.close()
    with pytest.raises(ValueError):
        budget.add_expense(exp)
    with pytest.raises(ValueError):
        budget.change_limit(1)

    s = SalaryPayment("SERR", Employee("E", "P", "E-9", 10), TODAY, FUTURE, 10)
    with pytest.raises(ValueError):
        s.add_bonus(0)
    with pytest.raises(ValueError):
        s.add_deduction(11)
    s.pay()
    with pytest.raises(PaymentError):
        s.cancel()
    with pytest.raises(ValueError):
        s.add_note("")

    empty_report = FinancialReport("ER", TODAY, FUTURE)
    with pytest.raises(ValueError):
        empty_report.add_note("")
    with pytest.raises(ValueError):
        empty_report.add_payment(
            Payment("OLD", o, 1, "cash", payment_date=TODAY - timedelta(days=10))
        )
    empty_report.finalize()
    with pytest.raises(ValueError):
        empty_report.finalize()
    with pytest.raises(ValueError):
        empty_report.add_note("late")


# ---------------- COMPANY ----------------
def test_employee_customer_order_registries():
    er = EmployeeRegistry()
    e = Employee("Елена", "1", "E-1", 1000)
    er.register(e)
    assert er.get_employee("E-1") is e
    assert er.find_by_name("ел") == [e]
    assert er.get_active_employees() == [e]
    assert er.get_by_department("Transport") == [e]
    assert er.calculate_total_salary() == 1000 and er.count_employees() == 1
    assert er.get_employee_ids() == ["E-1"]
    er.change_employee_status("E-1", False)
    assert er.get_active_employees() == []
    assert er.clear_inactive() == 1
    assert not er.unregister("missing")

    d = driver("D-REG")
    er.register(d)
    assert d in er.get_drivers()
    assert er.unregister("D-REG")

    cr = CustomerRegistry()
    c = customer("CR1")
    cr.register(c)
    assert cr.get_customer("CR1") is c
    assert cr.find_by_name("Иван") == [c]
    assert cr.get_active_customers() == [c]
    assert cr.get_customers_without_orders() == [c]
    assert cr.count_customers() == 1 and cr.calculate_total_orders() == 0
    cr.update_status("CR1", False)
    assert cr.get_active_customers() == []
    assert cr.unregister("CR1")

    c.activate()
    cr.register(c)
    o = order("CR-O", c)
    assert cr.get_customers_with_orders() == [c]
    assert cr.get_customer_order_history("CR1") == [o]
    assert cr.calculate_total_orders() == 1
    o.cancel()
    assert cr.unregister("CR1")

    orr = OrderRegistry()
    c2 = customer("CR2")
    o2 = order("OR1", c2)
    o2.set_priority("high")
    o2.set_delivery_deadline(FUTURE)
    orr.register(o2)
    assert orr.get_order("OR1") is o2
    assert orr.get_by_status("new") == [o2]
    assert orr.get_by_customer(c2) == [o2]
    assert orr.get_by_priority("high") == [o2]
    assert orr.count_orders() == 1 and orr.count_by_status("new") == 1
    assert orr.get_orders_for_period(TODAY - timedelta(days=1), FUTURE) == [o2]
    assert orr.get_order_statistics() == {"new": 1}
    orr.cancel_order("OR1")
    assert orr.unregister("OR1")
    assert not orr.unregister("unknown")


def test_fleet_warehouse_department_branch_and_policies():
    fleet = Fleet("F1", "Автопарк", 3)
    v = truck("F-V1")
    fleet.add_vehicle(v)
    assert fleet.get_vehicle("F-V1") is v
    assert fleet.get_available_vehicles() == [v]
    assert fleet.find_by_registration("REG-F-V1") is v
    assert fleet.get_vehicles_by_fuel("diesel") == [v]
    assert fleet.calculate_total_capacity() == 10000
    assert fleet.calculate_average_mileage() == 0

    d = driver("F-D1")
    fleet.assign_driver(d, "F-V1")
    assert d.assigned_vehicle is v
    with pytest.raises(InvalidDriverError):
        fleet.assign_driver(d, "F-V1")
    assert fleet.unassign_driver("F-D1")
    with pytest.raises(InvalidVehicleError):
        fleet.add_vehicle(v)
    v.mark_unavailable()
    with pytest.raises(VehicleUnavailableError):
        fleet.remove_vehicle("F-V1")
    v.mark_available()
    assert fleet.remove_vehicle("F-V1")
    fleet.activate()
    fleet.deactivate()

    wh = Warehouse("WH", "Склад", "Адрес", 1000)
    g = cargo("WH-G", 100, 2)
    wh.store_cargo(g)
    assert wh.get_cargo("WH-G") is g and wh.has_cargo("WH-G")
    assert wh.find_cargo_by_name("Груз") == [g]
    assert wh.get_cargo_count() == 1 and wh.get_total_cargo_value() == 1000
    assert wh.calculate_occupancy() == 10
    wh.reserve_capacity(100)
    assert wh.get_free_capacity() == 800
    wh.cancel_reservation(100)
    wh.change_manager(Manager("M", "1", "M-1", 1))
    wh.add_note("n")
    with pytest.raises(DeliveryError):
        wh.close_warehouse()
    assert wh.release_cargo("WH-G") is g
    wh.close_warehouse()
    with pytest.raises(DeliveryError):
        wh.store_cargo(cargo("WH-G2"))
    wh.open_warehouse()

    dep = Department("DEP", "Логистика")
    emp = Employee("A", "1", "DEP-E", 100)
    dep.add_employee(emp)
    dep.assign_manager(emp)
    dep.set_budget(1000)
    dep.set_monthly_target(5)
    ex = Expense("DEP-X", "x", "x", 20, TODAY)
    ex.approve(emp)
    dep.add_expense(ex)
    assert dep.calculate_expenses() == 20 and dep.calculate_remaining_budget() == 980
    assert dep.calculate_payroll() == 100 and dep.find_employee("DEP-E") is emp
    dep.assign_task("DEP-E", "task")
    dep.activate()
    dep.remove_employee(emp)
    dep.deactivate()
    dep.add_note("n")

    branch = Branch("BR", "Филиал", "Адрес", "123")
    be = Employee("B", "1", "BE", 200)
    branch.add_employee(be)
    branch.assign_manager(be)
    branch.add_vehicle(truck("BR-V"))
    branch.add_warehouse(Warehouse("BR-WH", "Склад", "A", 100))
    assert branch.find_employee("BE") is be
    assert branch.calculate_fleet_capacity() == 10000
    assert branch.calculate_available_capacity() == 10000
    assert branch.calculate_payroll() == 200
    branch.set_monthly_target(100)
    branch.remove_warehouse("BR-WH")
    branch.remove_vehicle(branch.vehicles[0])
    branch.remove_employee(be)
    branch.deactivate()
    branch.activate()
    branch.add_note("n")

    policy = CompanyPolicy(
        "POL", "Упаковка", "cargo", "Все упаковать", {"require_packed_cargo": True}, TODAY, FUTURE
    )
    o = order("POL-O")
    item = OrderItem("POL-I", cargo("POL-G"))
    o.add_item(item)
    assert policy.validate_order(o) == ["Все грузы должны быть упакованы."]
    assert not policy.check_order(o)
    item.cargo.pack()
    assert policy.check_order(o)
    policy.set_rule("max_order_weight_kg", 1000)
    assert policy.apply_to_order(o)
    policy.remove_rule("max_order_weight_kg")
    policy.add_note("n")
    policy.disable()
    assert not policy.is_effective()
    policy.enable()
    policy.extend_validity(FUTURE + timedelta(days=10))


def test_transport_company_orchestration():
    company = TransportCompany("CO", "ТК", "ТК ООО", "TAX", "Адрес", "123", "mail@test.ru")
    branch = Branch("B1", "Филиал", "Адрес", "123")
    company.add_branch(branch)
    assert company.get_branch("B1") is branch
    dep = Department("D1", "Отдел")
    company.add_department(dep)
    assert company.remove_department("D1")

    emp = Employee("С", "1", "E1", 100)
    company.register_employee(emp, "B1")
    assert emp in branch.employees
    new_branch = Branch("B2", "Филиал 2", "Адрес 2", "456")
    company.add_branch(new_branch)
    company.transfer_employee("E1", "B1", "B2")
    assert emp in new_branch.employees

    c = customer("C-CO")
    company.register_customer(c)
    o = order("O-CO", c)
    it = OrderItem("IT-CO", cargo("G-CO"))
    it.cargo.pack()
    it.set_unit_price(50)
    o.add_item(it)
    company.register_order(o)
    policy = CompanyPolicy("P-CO", "Обычная", "order", "без ограничений")
    company.add_policy(policy)
    company.approve_order("O-CO")
    assert o.status == "pending"
    o.approve()

    v = truck("CO-V")
    company.add_vehicle(v, "B2")
    d = driver("CO-D")
    company.register_employee(d)
    company.fleet.assign_driver(d, "CO-V")
    rt = route("CO-R")
    trip = Trip("CO-T", d, v, rt, datetime.now())
    company.assign_order_to_trip("O-CO", trip)
    assert trip in company.fleet.trip_history
    assert company.calculate_total_vehicle_capacity() == v.capacity_kg
    assert company.calculate_active_employee_count() == 2
    assert company.calculate_branch_count() == 2
    assert company.get_available_vehicles() == [v]
    assert company.get_active_orders()

    wh = Warehouse("CO-WH", "Склад", "Адрес", 1000)
    new_branch.add_warehouse(wh)
    assert company.calculate_total_warehouse_capacity() == 1000
    report = FinancialReport("CO-REP", TODAY, FUTURE)
    company.add_financial_report(report)
    assert company.get_latest_financial_report() is report
    summary = company.get_company_summary()
    assert summary["vehicles"] == 1 and summary["orders"] == 1
    company.activate()
    company.add_note("note")
    trip.start()
    with pytest.raises(DeliveryError):
        company.deactivate()
    trip.finish()
    company.deactivate()


def test_exception_classes_and_inheritance():
    exception_classes = [
        TransportCompanyError,
        InvalidCustomerError,
        InvalidDriverError,
        InvalidVehicleError,
        VehicleUnavailableError,
        DriverUnavailableError,
        InvalidCargoError,
        CargoCapacityExceededError,
        InvalidRouteError,
        InvalidOrderStatusError,
        PaymentError,
        DeliveryError,
    ]

    for exception_class in exception_classes:
        error = exception_class("test")
        assert isinstance(error, Exception)

    for exception_class in exception_classes[1:]:
        assert issubclass(exception_class, TransportCompanyError)


def test_company_registries_fleet_and_warehouse_error_branches():
    # EmployeeRegistry: validation, occupied driver protection, both statuses.
    er = EmployeeRegistry()
    with pytest.raises(InvalidDriverError):
        er.register(object())
    emp = Employee("A", "1", "E1", 1)
    er.register(emp)
    with pytest.raises(InvalidDriverError):
        er.register(emp)
    er.change_employee_status("E1", True)
    with pytest.raises(InvalidDriverError):
        er.change_employee_status("NO", True)
    busy_driver = driver("D-BUSY")
    busy_driver.assigned_vehicle = truck("ASSIGNED")
    er.register(busy_driver)
    with pytest.raises(InvalidDriverError):
        er.unregister("D-BUSY")
    busy_driver.deactivate()
    assert er.clear_inactive() == 0  # водитель с назначенной машиной остаётся

    # CustomerRegistry: missing/duplicate id, active orders, missing lookups.
    cr = CustomerRegistry()
    with pytest.raises(InvalidCustomerError):
        cr.register(object())
    c = customer("DUP-C")
    cr.register(c)
    with pytest.raises(InvalidCustomerError):
        cr.register(c)
    o = order("ACTIVE-C", c)
    with pytest.raises(InvalidCustomerError):
        cr.unregister("DUP-C")
    with pytest.raises(InvalidCustomerError):
        cr.get_customer_order_history("NONE")
    with pytest.raises(InvalidCustomerError):
        cr.update_status("NONE", True)
    cr.update_status("DUP-C", True)
    assert cr.get_corporate_customers() == []
    corporate = CorporateCustomer("ООО", "2", "Адрес", "TAX-CR")
    corporate.customer_id = "CORP-CR"
    cr.register(corporate)
    assert cr.get_corporate_customers() == [corporate]

    # OrderRegistry: missing/duplicate IDs, invalid removal and period.
    reg = OrderRegistry()
    with pytest.raises(InvalidOrderStatusError):
        reg.register(object())
    reg.register(o)
    with pytest.raises(InvalidOrderStatusError):
        reg.register(o)
    o.approve()
    with pytest.raises(InvalidOrderStatusError):
        reg.unregister(o.order_id)
    with pytest.raises(ValueError):
        reg.get_orders_for_period(FUTURE, TODAY)
    assert reg.get_overdue_orders(TODAY + timedelta(days=1)) == []
    assert reg.calculate_total_weight() == 0
    assert reg.calculate_total_value() == 0
    with pytest.raises(InvalidOrderStatusError):
        reg.cancel_order("missing")

    # Fleet: constructors, limits, assignment, maintenance and trip relations.
    with pytest.raises(ValueError):
        Fleet("", "x")
    with pytest.raises(ValueError):
        Fleet("F", "x", 0)
    fl = Fleet("F", "f", 1)
    with pytest.raises(InvalidVehicleError):
        fl.add_vehicle(object())
    v = truck("FL-V")
    fl.add_vehicle(v)
    with pytest.raises(InvalidVehicleError):
        fl.add_vehicle(truck("FL-V"))
    with pytest.raises(InvalidVehicleError):
        fl.add_vehicle(truck("FL-V2"))
    d = driver("FL-D")
    with pytest.raises(InvalidVehicleError):
        fl.assign_driver(d, "missing")
    v.mark_unavailable()
    with pytest.raises(VehicleUnavailableError):
        fl.assign_driver(d, "FL-V")
    v.mark_available()
    no_id_driver = type("DriverStub", (), {"employee_id": None})()
    with pytest.raises(InvalidDriverError):
        fl.assign_driver(no_id_driver, "FL-V")
    fl.assign_driver(d, "FL-V")
    with pytest.raises(InvalidVehicleError):
        fl.remove_vehicle("FL-V")
    d.is_available = False
    with pytest.raises(InvalidDriverError):
        fl.unassign_driver("FL-D")
    # Release correctly, then verify false return.
    d.is_available = True
    d.assigned_vehicle = None
    fl.assigned_drivers.pop("FL-D")
    assert not fl.unassign_driver("missing")

    rt = route("FL-R")
    d2 = driver("FL-D2")
    v2 = truck("FL-V3")
    d2.assign_vehicle(v2)
    trip = Trip("FL-T", d2, v2, rt, datetime.now())
    with pytest.raises(InvalidVehicleError):
        fl.register_trip(trip)
    trip_stub = type("TripStub", (), {"trip_id": "T", "vehicle": v})()
    fl.register_trip(trip_stub)
    with pytest.raises(ValueError):
        fl.register_trip(trip_stub)
    assert fl.get_vehicle_trips("FL-V")
    assert fl.get_vehicles_needing_inspection() == []
    with pytest.raises(InvalidVehicleError):
        fl.add_maintenance_record(MaintenanceRecord("X", v2, TODAY, "service", 1))
    fl.add_maintenance_record(MaintenanceRecord("OK", v, TODAY, "service", 1))
    fl.add_note("ok")
    with pytest.raises(ValueError):
        fl.add_note("")
    v.mark_unavailable()
    with pytest.raises(VehicleUnavailableError):
        fl.deactivate()
    v.mark_available()
    assert fl.remove_vehicle("FL-V")

    # Warehouse validations and negative paths.
    with pytest.raises(ValueError):
        Warehouse("", "x", "a", 1)
    with pytest.raises(ValueError):
        Warehouse("W", "x", "a", 0)
    wh = Warehouse("W-EDGE", "W", "a", 10)
    with pytest.raises(DeliveryError):
        wh.store_cargo(object())
    g = cargo("W-G", 10, 1)
    wh.store_cargo(g)
    with pytest.raises(DeliveryError):
        wh.store_cargo(g)
    with pytest.raises(DeliveryError):
        wh.store_cargo(cargo("W-G2", 1, 1))
    assert wh.release_cargo("unknown") is None
    with pytest.raises(ValueError):
        wh.reserve_capacity(-1)
    with pytest.raises(DeliveryError):
        wh.reserve_capacity(1)
    with pytest.raises(ValueError):
        wh.cancel_reservation(1)
    with pytest.raises(ValueError):
        wh.change_manager(None)
    with pytest.raises(ValueError):
        wh.add_note("")
    wh.release_cargo("W-G")
    assert wh.get_free_capacity() == 10


def test_department_branch_and_company_policy_edge_cases():
    with pytest.raises(ValueError):
        Department("", "x")
    with pytest.raises(ValueError):
        Department("D", "x", monthly_target=-1)
    dep = Department("D-EDGE", "Отдел")
    e = Employee("E", "1", "DE", 100)
    dep.add_employee(e)
    with pytest.raises(ValueError):
        dep.add_employee(e)
    with pytest.raises(ValueError):
        dep.assign_manager(Employee("X", "1", "X", 1))
    dep.change_manager(e)
    with pytest.raises(ValueError):
        dep.set_budget(-1)
    with pytest.raises(ValueError):
        dep.set_monthly_target(-1)
    assert not dep.remove_employee(Employee("N", "1", "N", 1))
    with pytest.raises(InvalidDriverError):
        dep.assign_task("no", "task")
    with pytest.raises(ValueError):
        dep.deactivate()
    dep.remove_employee(e)
    dep.activate()
    dep.deactivate()
    with pytest.raises(ValueError):
        dep.add_note("")

    with pytest.raises(ValueError):
        Branch("", "x", "a", "p")
    br = Branch("BR-EDGE", "Br", "Address", "phone")
    e1 = Employee("B", "1", "B-1", 10)
    br.add_employee(e1)
    with pytest.raises(ValueError):
        br.add_employee(e1)
    with pytest.raises(ValueError):
        br.assign_manager(Employee("X", "1", "X-2", 1))
    br.assign_manager(e1)
    assert not br.remove_employee(Employee("N", "1", "N-2", 1))
    v = truck("BR-EDGE-V")
    with pytest.raises(VehicleUnavailableError):
        busy = truck("BUSY-BR", False)
        br.add_vehicle(busy)
    br.add_vehicle(v)
    with pytest.raises(InvalidVehicleError):
        br.add_vehicle(v)
    v.mark_unavailable()
    with pytest.raises(VehicleUnavailableError):
        br.remove_vehicle(v)
    v.mark_available()
    assert not br.remove_vehicle(truck("NOT-THERE"))
    wh = Warehouse("BR-EDGE-W", "W", "addr", 10)
    br.add_warehouse(wh)
    with pytest.raises(ValueError):
        br.add_warehouse(wh)
    wh.store_cargo(cargo("BR-C", 1, 1))
    with pytest.raises(DeliveryError):
        br.remove_warehouse("BR-EDGE-W")
    assert br.find_employee("none") is None
    assert br.can_accept_order(order("BR-O"))
    br.deactivate()
    assert not br.can_accept_order(order("BR-O2"))
    with pytest.raises(ValueError):
        br.set_monthly_target(-1)
    v.mark_unavailable()
    with pytest.raises(VehicleUnavailableError):
        br.deactivate()
    v.mark_available()
    with pytest.raises(ValueError):
        br.add_note("")

    with pytest.raises(ValueError):
        CompanyPolicy("", "x", "x", "x")
    pol = CompanyPolicy(
        "POL-EDGE",
        "Policy",
        "cargo",
        "desc",
        {
            "max_order_weight_kg": 1,
            "max_cargo_items": 0,
            "max_order_value": 0,
            "allow_dangerous_cargo": False,
            "allow_oversized_cargo": False,
            "minimum_notice_days": 10,
        },
    )
    with pytest.raises(ValueError):
        pol.set_rule("", 1)
    pol.disable()
    with pytest.raises(ValueError):
        pol.set_rule("x", 1)
    assert not pol.remove_rule("not-there")
    assert not pol.is_effective(TODAY)
    pol.enable()
    o = order("POL-EDGE-O")
    dangerous = DangerousCargo("DG", "Chem", 5, 1, "3", "UN1")
    oversized = OversizedCargo("OS", "Beam", 5, 1, 3, 2, 1)
    for ix, item_cargo in enumerate([dangerous, oversized]):
        o.add_item(OrderItem(f"POL-EDGE-{ix}", item_cargo))
    o.set_delivery_deadline(TODAY + timedelta(days=1))
    violations = pol.validate_order(o)
    assert len(violations) >= 5
    pol.effective_until = TODAY - timedelta(days=1)
    assert not pol.check_order(o)
    with pytest.raises(InvalidOrderStatusError):
        pol.apply_to_order(o)
    with pytest.raises(ValueError):
        pol.extend_validity(TODAY - timedelta(days=2))
    with pytest.raises(ValueError):
        pol.add_note("")


def test_transport_company_error_and_empty_cases():
    with pytest.raises(ValueError):
        TransportCompany("", "x", "x", "id", "a", "p", "e")
    with pytest.raises(ValueError):
        TransportCompany("C", "x", "x", "", "a", "p", "e")
    co = TransportCompany("C-EDGE", "Company", "Legal", "TIN", "A", "P", "E")
    b = Branch("B-EDGE", "Branch", "A", "P")
    co.add_branch(b)
    with pytest.raises(ValueError):
        co.add_branch(b)
    assert not co.remove_branch("missing")
    b.add_employee(Employee("Resident", "1", "RES", 10))
    with pytest.raises(ValueError):
        co.remove_branch("B-EDGE")
    b2 = Branch("B-EMPTY", "Empty", "A", "P")
    co.add_branch(b2)
    assert co.remove_branch("B-EMPTY")

    dep = Department("D-EDGE", "D")
    co.add_department(dep)
    with pytest.raises(ValueError):
        co.add_department(dep)
    dep.add_employee(Employee("Department member", "1", "DEP-M", 10))
    with pytest.raises(ValueError):
        co.remove_department("D-EDGE")
    dep.remove_employee(dep.employees[0])
    assert co.remove_department("D-EDGE")
    assert not co.remove_department("no")

    e = Employee("E", "1", "E-EDGE", 1)
    with pytest.raises(ValueError):
        co.register_employee(e, "NO-BRANCH")
    assert co.employee_registry.get_employee("E-EDGE") is None  # rollback

    c = customer("CO-EDGE-C")
    co.register_customer(c)
    other = customer("OTHER-C")
    bad_order = order("CO-BAD-ORDER", other)
    with pytest.raises(InvalidCustomerError):
        co.register_order(bad_order)

    with pytest.raises(ValueError):
        co.add_vehicle(truck("CO-BAD-V"), "NO-BRANCH")
    assert co.fleet.get_vehicle("CO-BAD-V") is None  # rollback

    p = CompanyPolicy("P-EDGE", "P", "x", "x")
    co.add_policy(p)
    with pytest.raises(ValueError):
        co.add_policy(p)
    assert not co.remove_policy("missing")
    assert co.remove_policy("P-EDGE")
    with pytest.raises(InvalidOrderStatusError):
        co.approve_order("missing")
    with pytest.raises(InvalidOrderStatusError):
        co.assign_order_to_trip("missing", make_trip())

    valid_customer = customer("CO-VALID")
    co.register_customer(valid_customer)
    o = order("CO-ORDER", valid_customer)
    item = OrderItem("CO-ITEM", cargo("CO-CARGO"))
    item.cargo.pack()
    o.add_item(item)
    co.register_order(o)
    strict = CompanyPolicy("STRICT", "Strict", "cargo", "packed", {"max_order_weight_kg": 1})
    co.add_policy(strict)
    with pytest.raises(InvalidOrderStatusError):
        co.approve_order(o.order_id)
    strict.disable()
    co.approve_order(o.order_id)
    o.approve()
    with pytest.raises(InvalidVehicleError):
        co.assign_order_to_trip(o.order_id, make_trip("OUTSIDE"))

    with pytest.raises(InvalidDriverError):
        co.transfer_employee("none", "B-EDGE", "B-EDGE")
    with pytest.raises(ValueError):
        co.transfer_employee("E-EDGE", "none", "B-EDGE")
    co.register_employee(e)
    with pytest.raises(ValueError):
        co.transfer_employee("E-EDGE", "B-EDGE", "B-EDGE")
    dest = Branch("B-DES", "Dest", "A", "P")
    dest.deactivate()
    co.add_branch(dest)
    src = Branch("B-SRC", "Src", "A", "P")
    src.add_employee(e)
    co.add_branch(src)
    with pytest.raises(ValueError):
        co.transfer_employee("E-EDGE", "B-SRC", "B-DES")
    assert co.get_latest_financial_report() is None
    empty_rep = FinancialReport("EMPTY-REP", TODAY, FUTURE)
    co.add_financial_report(empty_rep)
    with pytest.raises(ValueError):
        co.add_financial_report(empty_rep)
    with pytest.raises(ValueError):
        co.add_note("")


def test_finance_remaining_validation_and_state_branches():
    o = order("FIN-EDGE")
    item = OrderItem("FE-I", cargo("FE-G"))
    item.set_unit_price(100)
    o.add_item(item)

    with pytest.raises(ValueError):
        Payment("", o, 1, "cash")
    with pytest.raises(ValueError):
        Payment("P", o, 0, "cash")
    with pytest.raises(ValueError):
        Payment("P", o, 1, "")
    p = Payment("P-EDGE", o, 100, "cash")
    with pytest.raises(ValueError):
        p.change_payment_method("")
    with pytest.raises(ValueError):
        p.add_note("")
    p.fail("отказ")
    with pytest.raises(PaymentError):
        p.fail("ещё раз")
    with pytest.raises(PaymentError):
        p.refund()

    completed = Payment("P-COMP", o, 100, "cash")
    completed.status = "completed"
    with pytest.raises(PaymentError):
        completed.fail("late")
    with pytest.raises(PaymentError):
        completed.refund(0)
    with pytest.raises(PaymentError):
        completed.refund(101)
    completed.refund(20)
    assert completed.status == "partially_refunded"

    with pytest.raises(ValueError):
        Invoice("", o, FUTURE)
    with pytest.raises(ValueError):
        Invoice("I", o, FUTURE, tax_rate=1.1)
    with pytest.raises(ValueError):
        Invoice("I", o, FUTURE, discount_amount=-1)
    invoice = Invoice("INV-EDGE", o, TODAY - timedelta(days=1))
    with pytest.raises(ValueError):
        invoice.issue()
    invoice.due_date = FUTURE
    invoice.issue()
    assert invoice.is_overdue(FUTURE + timedelta(days=1))
    assert not invoice.can_accept_payment(0)
    with pytest.raises(PaymentError):
        invoice.add_charge("fee", 1)
    with pytest.raises(PaymentError):
        invoice.apply_discount(1)
    with pytest.raises(PaymentError):
        invoice.issue()
    with pytest.raises(ValueError):
        invoice.update_due_date(TODAY - timedelta(days=1))
    invoice.update_due_date(FUTURE + timedelta(days=5))
    with pytest.raises(ValueError):
        invoice.add_note("")

    unattached = Payment("P-WRONG", o, 10, "cash")
    with pytest.raises(PaymentError):
        invoice.register_payment(unattached)
    unprocessed = Payment("P-PENDING", o, 10, "cash", invoice)
    with pytest.raises(PaymentError):
        invoice.register_payment(unprocessed)
    overpay = Payment("P-OVER", o, 101, "cash", invoice)
    overpay.status = "completed"
    with pytest.raises(PaymentError):
        invoice.register_payment(overpay)
    accepted = Payment("P-OK", o, 40, "cash", invoice)
    accepted.status = "completed"
    invoice.register_payment(accepted)
    assert invoice.status == "partially_paid"
    with pytest.raises(PaymentError):
        invoice.register_payment(accepted)
    with pytest.raises(PaymentError):
        invoice.cancel()
    with pytest.raises(PaymentError):
        invoice.register_refund(0)
    invoice.register_refund(40)
    assert invoice.amount_paid == 0 and invoice.status == "issued"
    paid_invoice = Invoice("INV-PAID", o, FUTURE)
    paid_invoice.status = "paid"
    with pytest.raises(PaymentError):
        paid_invoice.update_due_date(FUTURE)

    with pytest.raises(ValueError):
        Transaction("", completed, "payment", 1)
    with pytest.raises(ValueError):
        Transaction("X", completed, "other", 1)
    with pytest.raises(ValueError):
        Transaction("X", completed, "payment", 0)
    tr = Transaction("TX-EDGE", completed, "payment", 1)
    with pytest.raises(ValueError):
        tr.set_external_reference("")
    tr.mark_successful()
    with pytest.raises(PaymentError):
        tr.mark_successful()
    with pytest.raises(PaymentError):
        tr.mark_failed("again")
    tr2 = Transaction("TX-FAIL", completed, "payment", 1)
    tr2.mark_failed("declined")
    with pytest.raises(PaymentError):
        tr2.mark_failed("again")
    with pytest.raises(PaymentError):
        tr2.reverse("not successful")

    with pytest.raises(ValueError):
        Expense("", "fuel", "d", 1)
    with pytest.raises(ValueError):
        Expense("X", "", "d", 1)
    with pytest.raises(ValueError):
        Expense("X", "fuel", "d", 0)
    pending = Expense("EX-EDGE", "fuel", "desc", 10, TODAY)
    with pytest.raises(ValueError):
        pending.approve(None)
    pending.reject("no")
    with pytest.raises(ValueError):
        pending.reject("again")
    with pytest.raises(ValueError):
        pending.mark_reimbursed()
    with pytest.raises(ValueError):
        pending.update_amount(1)
    with pytest.raises(ValueError):
        pending.change_category("x")

    with pytest.raises(ValueError):
        Budget("", "fuel", 1, TODAY, FUTURE)
    with pytest.raises(ValueError):
        Budget("B", "", 1, TODAY, FUTURE)
    with pytest.raises(ValueError):
        Budget("B", "fuel", -1, TODAY, FUTURE)
    with pytest.raises(ValueError):
        Budget("B", "fuel", 1, FUTURE, TODAY)
    budget = Budget("B-EDGE", "fuel", 100, TODAY, FUTURE)
    with pytest.raises(ValueError):
        budget.add_expense(Expense("OUTSIDE", "fuel", "x", 1, FUTURE + timedelta(days=1)))
    in_range = Expense("IN", "fuel", "x", 10, TODAY)
    budget.add_expense(in_range)
    with pytest.raises(ValueError):
        budget.add_expense(in_range)
    assert not budget.remove_expense("unknown")
    with pytest.raises(ValueError):
        budget.change_limit(-1)
    budget.close()
    with pytest.raises(ValueError):
        budget.close()
    with pytest.raises(ValueError):
        budget.change_limit(1)
    budget.reopen()
    with pytest.raises(ValueError):
        budget.reopen()
    with pytest.raises(ValueError):
        budget.add_note("")
    zero = Budget("B-ZERO", "zero", 0, TODAY, FUTURE)
    zero_expense = Expense("ZE", "zero", "z", 1, TODAY)
    zero_expense.approve(object())
    zero.add_expense(zero_expense)
    assert zero.get_usage_percentage() == 100

    employee = Employee("E", "1", "SAL-E", 100)
    with pytest.raises(ValueError):
        SalaryPayment("", employee, TODAY, FUTURE, 100)
    with pytest.raises(ValueError):
        SalaryPayment("S", employee, FUTURE, TODAY, 100)
    with pytest.raises(ValueError):
        SalaryPayment("S", employee, TODAY, FUTURE, -1)
    salary = SalaryPayment("SAL-EDGE", employee, TODAY, FUTURE, 100)
    with pytest.raises(ValueError):
        salary.add_deduction(0)
    salary.add_deduction(100)
    salary.bonus = 0
    salary.deductions = 101
    with pytest.raises(PaymentError):
        salary.pay()
    salary.status = "paid"
    with pytest.raises(ValueError):
        salary.add_bonus(1)
    with pytest.raises(ValueError):
        salary.add_deduction(1)
    with pytest.raises(PaymentError):
        salary.cancel()

    with pytest.raises(ValueError):
        FinancialReport("", TODAY, FUTURE)
    with pytest.raises(ValueError):
        FinancialReport("R", FUTURE, TODAY)
    report = FinancialReport("R-EDGE", TODAY, FUTURE)
    assert report._to_date(None) is None
    assert report._to_date(datetime.now()) == TODAY
    assert not report._is_in_period(None)
    with pytest.raises(ValueError):
        report.add_expense(Expense("OUT-R", "fuel", "x", 1, FUTURE + timedelta(days=1)))
    with pytest.raises(ValueError):
        report.add_salary_payment(SalaryPayment("NOT-PAID", employee, TODAY, FUTURE, 1))
    payment = Payment("P-REP", o, 1, "cash", payment_date=TODAY)
    report.add_payment(payment)
    with pytest.raises(ValueError):
        report.add_payment(payment)
    expense = Expense("E-REP", "fuel", "x", 1, TODAY)
    report.add_expense(expense)
    with pytest.raises(ValueError):
        report.add_expense(expense)
    report.finalize()
    with pytest.raises(ValueError):
        report.add_payment(payment)
    with pytest.raises(ValueError):
        report.add_expense(expense)
    with pytest.raises(ValueError):
        report.add_salary_payment(salary)


def test_transport_remaining_validation_and_conflict_branches():
    # Constructor validation and empty-state behaviour.
    with pytest.raises(InvalidRouteError):
        RoutePoint("P", "A", 0)
    with pytest.raises(InvalidRouteError):
        Route("", "name", "A", "B", 10)
    empty_route = route("EMPTY-ROUTE")
    assert empty_route.get_next_point() is None
    assert empty_route.progress_percentage() == 100
    with pytest.raises(InvalidCargoError):
        OrderItem("", cargo())
    with pytest.raises(InvalidCargoError):
        OrderItem("BAD-Q", cargo(), 0)
    with pytest.raises(InvalidCargoError):
        OrderItem("BAD-PRICE", cargo()).set_unit_price(-1)
    with pytest.raises(InvalidOrderStatusError):
        TransportOrder("", customer(), "A", "B")

    # Route and order mutations.
    c = customer("TR-EDGE-C")
    o = TransportOrder("TR-EDGE-O", c, "Москва", "Тверь")
    item = OrderItem("TR-EDGE-I", cargo("TR-EDGE-G"))
    o.add_item(item)
    assert o.remove_item("TR-EDGE-I")
    assert not o.remove_item("none")
    with pytest.raises(InvalidOrderStatusError):
        o.set_status("not-a-status")
    inactive_route = route("INACTIVE")
    inactive_route.set_active(False)
    with pytest.raises(InvalidRouteError):
        o.set_route(inactive_route)
    with pytest.raises(InvalidRouteError):
        o.set_route(Route("OTHER", "other", "X", "Y", 1))
    with pytest.raises(InvalidOrderStatusError):
        o.set_priority("critical")
    with pytest.raises(InvalidOrderStatusError):
        o.set_delivery_deadline(TODAY - timedelta(days=1))
    wrong_customer = customer("TR-OTHER-C")
    bad_order = TransportOrder("TR-BAD-ORDER", wrong_customer, "A", "B")
    with pytest.raises(InvalidOrderStatusError):
        bad_order.assign_trip(object())

    # Shipment preconditions and all transport compatibility checks.
    empty_shipment = Shipment("SH-EMPTY", order("SH-EMPTY-O"))
    with pytest.raises(DeliveryError):
        empty_shipment.load_onto(truck("SH-NOT-READY"))
    with pytest.raises(DeliveryError):
        empty_shipment.unload()
    with pytest.raises(DeliveryError):
        empty_shipment.set_seal_number("")
    packed_order = order("SH-PACK-O")
    packed_cargo = cargo("SH-PACK-G", 100, 5)
    packed_cargo.pack()
    packed_order.add_item(OrderItem("SH-PACK-I", packed_cargo))
    shipment = Shipment("SH-PACK", packed_order)
    shipment.prepare()
    busy_vehicle = truck("SH-BUSY", False)
    with pytest.raises(VehicleUnavailableError):
        shipment.load_onto(busy_vehicle)
    tanker = Tanker("SH-TANK", "M", "T", 2020, "SH-TANK", 1000, 100)
    with pytest.raises(InvalidCargoError):
        shipment.load_onto(tanker)
    low_capacity = truck("SH-LOW")
    low_capacity.capacity_kg = 10
    with pytest.raises(CargoCapacityExceededError):
        shipment.load_onto(low_capacity)
    oversized_volume_order = order("SH-VOL-O")
    vol_cargo = cargo("SH-VOL-G", 1, 100)
    vol_cargo.pack()
    oversized_volume_order.add_item(OrderItem("SH-VOL-I", vol_cargo))
    vol_shipment = Shipment("SH-VOL", oversized_volume_order)
    vol_shipment.prepare()
    small_body = truck("SH-SMALL")
    small_body.cargo_volume_m3 = 1
    with pytest.raises(CargoCapacityExceededError):
        vol_shipment.load_onto(small_body)

    # Stop validations.
    with pytest.raises(InvalidRouteError):
        Stop("", "address")
    with pytest.raises(InvalidRouteError):
        Stop("ST-BAD", "address", "shopping")
    st = Stop("ST-EDGE", "address")
    with pytest.raises(InvalidRouteError):
        st.schedule(datetime.now(), -1)
    assert st.delay_minutes() == 0
    with pytest.raises(InvalidRouteError):
        st.add_note("")

    # Trip validations: unapproved order, route mismatch, duplicate stop.
    rt = route("TRIP-EDGE-R")
    d = driver("TRIP-EDGE-D")
    v = truck("TRIP-EDGE-V")
    d.assign_vehicle(v)
    trip = Trip("TRIP-EDGE", d, v, rt, datetime.now())
    not_approved = order("TRIP-NO-APP")
    with pytest.raises(InvalidOrderStatusError):
        trip.add_order(not_approved)
    approved_wrong_route = order("TRIP-WRONG-ROUTE", status="approved")
    approved_wrong_route.set_route(Route("DIFF", "diff", "Москва", "Тверь", 20))
    with pytest.raises(InvalidRouteError):
        trip.add_order(approved_wrong_route)
    assigned_elsewhere = order("TRIP-ASSIGNED", status="approved")
    assigned_elsewhere.assigned_trip = object()
    with pytest.raises(InvalidOrderStatusError):
        trip.add_order(assigned_elsewhere)
    st1 = Stop("DUP-ST", "address")
    trip.add_stop(st1)
    with pytest.raises(InvalidRouteError):
        trip.add_stop(Stop("DUP-ST", "address"))
    with pytest.raises(InvalidRouteError):
        Trip("", d, v, rt, datetime.now())
    inactive = route("INACTIVE-TRIP")
    inactive.set_active(False)
    with pytest.raises(InvalidRouteError):
        Trip("BAD-TRIP", d, v, inactive, datetime.now())

    with pytest.raises(InvalidOrderStatusError):
        trip.finish()
    # Vehicle unavailable is checked before driver state.
    v.mark_unavailable()
    with pytest.raises(VehicleUnavailableError):
        trip.start()
    v.mark_available()
    d.is_available = False
    with pytest.raises(DriverUnavailableError):
        trip.start()
    d.is_available = True
    d.assigned_vehicle = None
    with pytest.raises(DriverUnavailableError):
        trip.start()
    d.assigned_vehicle = v
    trip.start()
    with pytest.raises(InvalidOrderStatusError):
        trip.start()
    with pytest.raises(InvalidOrderStatusError):
        trip.cancel()
    trip.finish()

    # Schedule detects same driver/vehicle conflict and ignores finished trips.
    with pytest.raises(InvalidRouteError):
        Schedule("", "name")
    when = datetime.now() + timedelta(days=1)
    sd = driver("SCHED-D")
    sv1 = truck("SCHED-V1")
    sd.assign_vehicle(sv1)
    first = Trip("SCHED-1", sd, sv1, rt, when)
    schedule = Schedule("SCHED", "Schedule")
    schedule.add_trip(first)
    conflict = Trip("SCHED-2", sd, truck("SCHED-V2"), rt, when)
    with pytest.raises(InvalidRouteError):
        schedule.add_trip(conflict)
    first.status = "completed"
    schedule.add_trip(conflict)  # завершённый рейс не блокирует ресурсы
    assert schedule.remove_trip("SCHED-2")
    assert not schedule.remove_trip("missing")
    schedule.add_trip(conflict)
    conflict.status = "in_progress"
    with pytest.raises(InvalidRouteError):
        schedule.remove_trip("SCHED-2")
    schedule.is_active = False
    with pytest.raises(InvalidRouteError):
        schedule.add_trip(Trip("SCHED-3", sd, truck("SCHED-V3"), rt, when + timedelta(hours=2)))

    # Delivery preconditions and terminal-state restrictions.
    with pytest.raises(DeliveryError):
        Delivery("", order("D-EMPTY"), "R", "A", TODAY)
    delivery = Delivery("D-EDGE", order("D-ORDER"), "R", "A", TODAY)
    with pytest.raises(DeliveryError):
        delivery.confirm_delivery("R")
    delivery.mark_in_transit()
    with pytest.raises(DeliveryError):
        delivery.mark_in_transit()
    with pytest.raises(DeliveryError):
        delivery.confirm_delivery("")
    delivery.confirm_delivery("R")
    with pytest.raises(DeliveryError):
        delivery.report_failure("failed")
    with pytest.raises(DeliveryError):
        delivery.reschedule(FUTURE)
    with pytest.raises(DeliveryError):
        delivery.record_recipient("")
