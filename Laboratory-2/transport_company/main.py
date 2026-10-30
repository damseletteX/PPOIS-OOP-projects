"""Консольный интерфейс системы управления транспортной компанией.

Запуск из папки проекта:
    python main.py
"""

from datetime import date, datetime

try:  # Импорт при запуске пакета
    from .company import TransportCompany
    from .people import (
        IndividualCustomer, CorporateCustomer, Employee,
        Driver, Dispatcher, Manager,
    )
    from .vehicles import (
        Vehicle, Truck, Van, RefrigeratedTruck, Tanker, FlatbedTruck,
    )
    from .cargo import (
        Cargo, PerishableCargo, FragileCargo, DangerousCargo, OversizedCargo,
    )
    from .transport import Route, TransportOrder, OrderItem, Trip
    from .finance import Invoice, Payment
except ImportError:  # Запуск командой python main.py из папки проекта
    from company import TransportCompany
    from people import (
        IndividualCustomer, CorporateCustomer, Employee,
        Driver, Dispatcher, Manager,
    )
    from vehicles import (
        Vehicle, Truck, Van, RefrigeratedTruck, Tanker, FlatbedTruck,
    )
    from cargo import (
        Cargo, PerishableCargo, FragileCargo, DangerousCargo, OversizedCargo,
    )
    from transport import Route, TransportOrder, OrderItem, Trip
    from finance import Invoice, Payment


class ConsoleApp:
    """Организует меню и взаимодействие пользователя с объектами проекта."""

    def __init__(self):
        self.company = self._create_company()
        self.cargos = {}
        self.routes = {}
        self.trips = {}
        self.invoices = {}

    @staticmethod
    def read_text(prompt: str, default: str | None = None) -> str:
        suffix = f" [{default}]" if default is not None else ""
        value = input(f"{prompt}{suffix}: ").strip()
        return value if value else (default if default is not None else "")

    @staticmethod
    def read_int(prompt: str, minimum: int | None = None) -> int:
        while True:
            try:
                value = int(input(f"{prompt}: "))
                if minimum is not None and value < minimum:
                    print(f"Введите целое число не меньше {minimum}.")
                    continue
                return value
            except ValueError:
                print("Ошибка: введите целое число.")

    @staticmethod
    def read_float(prompt: str, minimum: float | None = None) -> float:
        while True:
            try:
                value = float(input(f"{prompt}: ").replace(",", "."))
                if minimum is not None and value < minimum:
                    print(f"Введите число не меньше {minimum}.")
                    continue
                return value
            except ValueError:
                print("Ошибка: введите число.")

    @staticmethod
    def read_date(prompt: str) -> date:
        while True:
            raw = input(f"{prompt} (ГГГГ-ММ-ДД): ").strip()
            try:
                return date.fromisoformat(raw)
            except ValueError:
                print("Неверный формат. Пример: 2026-12-31.")

    @staticmethod
    def pause():
        input("\nНажмите Enter, чтобы продолжить...")

    @staticmethod
    def print_header(title: str):
        print("\n" + "=" * 58)
        print(title)
        print("=" * 58)

    @staticmethod
    def select_from_dict(items: dict, prompt: str):
        """Выбор объекта из словаря по ID. Возвращает (id, объект) или (None, None)."""
        if not items:
            print("Список пока пуст.")
            return None, None

        for item_id, item in items.items():
            name = getattr(item, "name", None) or getattr(item, "brand", "")
            print(f"{item_id}: {name or item.__class__.__name__}")

        selected_id = input(f"{prompt}: ").strip()
        item = items.get(selected_id)
        if item is None:
            print("Объект с таким ID не найден.")
            return None, None
        return selected_id, item

    def _create_company(self):
        self.print_header("Настройка транспортной компании")
        name = self.read_text("Название компании", "Транспортная компания")
        legal_name = self.read_text("Юридическое название", name)
        tax_id = self.read_text("Налоговый номер", "0000000000")
        address = self.read_text("Адрес", "Не указан")
        phone = self.read_text("Телефон", "+0000000000")
        email = self.read_text("Email", "info@example.com")
        return TransportCompany(
            company_id="COMP-001",
            name=name,
            legal_name=legal_name,
            tax_id=tax_id,
            address=address,
            phone=phone,
            email=email,
        )

    # ---------- Клиенты ----------

    def customers_menu(self):
        while True:
            self.print_header("КЛИЕНТЫ")
            print("1. Добавить частного клиента")
            print("2. Добавить корпоративного клиента")
            print("3. Показать клиентов")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "1":
                    customer_id = self.read_text("ID клиента")
                    customer = IndividualCustomer(
                        name=self.read_text("ФИО"),
                        phone=self.read_text("Телефон"),
                        address=self.read_text("Адрес"),
                        email=self.read_text("Email", ""),
                        passport_number=self.read_text("Номер паспорта", ""),
                    )
                    # В people.py у Customer нет ID в конструкторе,
                    # поэтому добавляем его при регистрации в реестре.
                    customer.customer_id = customer_id
                    self.company.register_customer(customer)
                    print("Клиент зарегистрирован.")
                elif choice == "2":
                    customer_id = self.read_text("ID клиента")
                    customer = CorporateCustomer(
                        name=self.read_text("Название организации"),
                        phone=self.read_text("Телефон"),
                        address=self.read_text("Адрес"),
                        tax_number=self.read_text("Регистрационный номер"),
                        email=self.read_text("Email", ""),
                    )
                    customer.customer_id = customer_id
                    self.company.register_customer(customer)
                    print("Корпоративный клиент зарегистрирован.")
                elif choice == "3":
                    for customer_id, customer in self.company.customer_registry.customers.items():
                        print(f"{customer_id}: {customer.name}, {customer.phone}, {customer.address}")
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()

    def employees_menu(self):
        while True:
            self.print_header("СОТРУДНИКИ")
            print("1. Добавить водителя")
            print("2. Добавить обычного сотрудника")
            print("3. Добавить диспетчера")
            print("4. Добавить менеджера")
            print("5. Показать сотрудников")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice in {"1", "2", "3", "4"}:
                    name = self.read_text("ФИО")
                    phone = self.read_text("Телефон")
                    employee_id = self.read_text("Табельный номер")
                    salary = self.read_float("Зарплата", 0)
                    email = self.read_text("Email", "")

                    if choice == "1":
                        categories = self.read_text(
                            "Категории прав через запятую (например B,C)"
                        )
                        employee = Driver(
                            name, phone, employee_id, salary,
                            self.read_text("Номер водительского удостоверения"),
                            [item.strip() for item in categories.split(",") if item.strip()],
                            self.read_int("Стаж в годах", 0), email,
                        )
                    elif choice == "2":
                        employee = Employee(name, phone, employee_id, salary, email)
                    elif choice == "3":
                        employee = Dispatcher(name, phone, employee_id, salary, email)
                    else:
                        employee = Manager(name, phone, employee_id, salary, email)

                    self.company.register_employee(employee)
                    print("Сотрудник зарегистрирован.")
                elif choice == "5":
                    for employee_id, employee in self.company.employee_registry.employees.items():
                        print(
                            f"{employee_id}: {employee.name} "
                            f"({employee.__class__.__name__}), "
                            f"зарплата: {employee.salary}, активен: {employee.is_active}"
                        )
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()


    def vehicles_menu(self):
        while True:
            self.print_header("АВТОПАРК")
            print("1. Добавить обычный транспорт")
            print("2. Добавить грузовик")
            print("3. Добавить фургон")
            print("4. Добавить рефрижератор")
            print("5. Добавить автоцистерну")
            print("6. Добавить платформенный грузовик")
            print("7. Показать транспорт")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice in {"1", "2", "3", "4", "5", "6"}:
                    vehicle_id = self.read_text("ID транспорта")
                    brand = self.read_text("Марка")
                    model = self.read_text("Модель")
                    year = self.read_int("Год выпуска", 1900)
                    registration = self.read_text("Регистрационный номер")
                    capacity = self.read_float("Грузоподъёмность (кг)", 0.01)
                    license_category = self.read_text("Категория прав", "B")
                    fuel_type = self.read_text("Тип топлива", "diesel")

                    if choice == "1":
                        vehicle = Vehicle(
                            vehicle_id, brand, model, year, registration,
                            capacity, license_category, fuel_type,
                        )
                    elif choice in {"2", "3", "4", "6"}:
                        volume = self.read_float("Объём кузова (м³)", 0.01)
                        if choice == "2":
                            vehicle = Truck(
                                vehicle_id, brand, model, year, registration,
                                capacity, volume, license_category, fuel_type,
                            )
                        elif choice == "3":
                            vehicle = Van(
                                vehicle_id, brand, model, year, registration,
                                capacity, volume, license_category, fuel_type,
                            )
                        elif choice == "4":
                            min_temp = self.read_float("Минимальная температура")
                            max_temp = self.read_float("Максимальная температура")
                            vehicle = RefrigeratedTruck(
                                vehicle_id, brand, model, year, registration,
                                capacity, volume, min_temp, max_temp,
                                license_category, fuel_type,
                            )
                        else:
                            length = self.read_float("Длина платформы (м)", 0.01)
                            vehicle = FlatbedTruck(
                                vehicle_id, brand, model, year, registration,
                                capacity, volume, length, license_category, fuel_type,
                            )
                    else:
                        tank_volume = self.read_float("Объём цистерны (л)", 0.01)
                        vehicle = Tanker(
                            vehicle_id, brand, model, year, registration,
                            capacity, tank_volume, license_category, fuel_type,
                        )

                    self.company.add_vehicle(vehicle)
                    print("Транспорт добавлен в автопарк.")
                elif choice == "7":
                    for vehicle_id, vehicle in self.company.fleet.vehicles.items():
                        print(
                            f"{vehicle_id}: {vehicle}, доступен: {vehicle.is_available}, "
                            f"пробег: {vehicle.mileage_km} км"
                        )
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()

    # ---------- Грузы ----------

    def cargo_menu(self):
        while True:
            self.print_header("ГРУЗЫ")
            print("1. Добавить обычный груз")
            print("2. Добавить скоропортящийся груз")
            print("3. Добавить хрупкий груз")
            print("4. Добавить опасный груз")
            print("5. Добавить негабаритный груз")
            print("6. Показать грузы")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice in {"1", "2", "3", "4", "5"}:
                    cargo_id = self.read_text("ID груза")
                    name = self.read_text("Название груза")
                    weight = self.read_float("Вес (кг)", 0.01)
                    volume = self.read_float("Объём (м³)", 0.01)
                    value = self.read_float("Объявленная стоимость", 0)
                    description = self.read_text("Описание", "")

                    if choice == "1":
                        cargo = Cargo(cargo_id, name, weight, volume, value, description)
                    elif choice == "2":
                        cargo = PerishableCargo(
                            cargo_id, name, weight, volume,
                            self.read_date("Срок годности"),
                            self.read_float("Температура хранения"), value, description,
                        )
                    elif choice == "3":
                        cargo = FragileCargo(
                            cargo_id, name, weight, volume,
                            self.read_int("Уровень хрупкости (1-5)", 1), value, description,
                        )
                    elif choice == "4":
                        cargo = DangerousCargo(
                            cargo_id, name, weight, volume,
                            self.read_text("Класс опасности"),
                            self.read_text("Номер ООН"), value, description,
                        )
                    else:
                        cargo = OversizedCargo(
                            cargo_id, name, weight, volume,
                            self.read_float("Длина (м)", 0.01),
                            self.read_float("Ширина (м)", 0.01),
                            self.read_float("Высота (м)", 0.01),
                            value, description,
                        )

                    if cargo_id in self.cargos:
                        raise ValueError("Груз с таким ID уже существует.")
                    self.cargos[cargo_id] = cargo
                    print("Груз добавлен.")
                elif choice == "6":
                    for cargo_id, cargo in self.cargos.items():
                        print(f"{cargo_id}: {cargo}, статус: {cargo.status}, упакован: {cargo.is_packed}")
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()

    # ---------- Заказы ----------

    def orders_menu(self):
        while True:
            self.print_header("ЗАКАЗЫ")
            print("1. Создать заказ и добавить грузы")
            print("2. Согласовать заказ")
            print("3. Показать заказы")
            print("4. Отменить заказ")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "1":
                    customer_id, customer = self.select_from_dict(
                        self.company.customer_registry.customers,
                        "Введите ID клиента",
                    )
                    if customer is None:
                        self.pause()
                        continue

                    order_id = self.read_text("ID заказа")
                    order = TransportOrder(
                        order_id,
                        customer,
                        self.read_text("Адрес отправления"),
                        self.read_text("Адрес назначения"),
                    )

                    while self.cargos:
                        print("\nДоступные грузы:")
                        for cargo_id, cargo in self.cargos.items():
                            print(f"{cargo_id}: {cargo.name} ({cargo.weight_kg} кг)")
                        cargo_id = input("ID груза для добавления (Enter — закончить): ").strip()
                        if not cargo_id:
                            break
                        cargo = self.cargos.get(cargo_id)
                        if cargo is None:
                            print("Груз не найден.")
                            continue
                        quantity = self.read_int("Количество", 1)
                        item = OrderItem(f"{order_id}-ITEM-{len(order.items) + 1}", cargo, quantity)
                        item.set_unit_price(self.read_float("Цена за единицу", 0))
                        order.add_item(item)
                        print("Позиция добавлена.")

                    if not order.items:
                        print("Заказ без позиций не зарегистрирован.")
                    else:
                        self.company.register_order(order)
                        print(
                            f"Заказ зарегистрирован. Вес: {order.total_weight()} кг; "
                            f"стоимость: {order.calculate_items_cost()}"
                        )
                elif choice == "2":
                    order_id, order = self.select_from_dict(
                        self.company.order_registry.orders,
                        "ID заказа",
                    )
                    if order is not None:
                        if order.status == "new":
                            self.company.approve_order(order_id)
                        if order.status == "pending":
                            order.approve()
                        print(f"Текущий статус заказа: {order.status}")
                elif choice == "3":
                    for order_id, order in self.company.order_registry.orders.items():
                        print(
                            f"{order_id}: {order.customer.name}, {order.origin} → "
                            f"{order.destination}, статус: {order.status}, "
                            f"вес: {order.total_weight()} кг"
                        )
                elif choice == "4":
                    order_id, order = self.select_from_dict(
                        self.company.order_registry.orders,
                        "ID заказа",
                    )
                    if order is not None:
                        order.cancel("Отмена через консольное меню")
                        print("Заказ отменён.")
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()

    # ---------- Маршруты и рейсы ----------

    def trips_menu(self):
        while True:
            self.print_header("МАРШРУТЫ И РЕЙСЫ")
            print("1. Создать маршрут")
            print("2. Создать рейс")
            print("3. Назначить заказ на рейс")
            print("4. Начать рейс")
            print("5. Завершить рейс")
            print("6. Показать маршруты и рейсы")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "1":
                    route_id = self.read_text("ID маршрута")
                    route = Route(
                        route_id,
                        self.read_text("Название маршрута"),
                        self.read_text("Откуда"),
                        self.read_text("Куда"),
                        self.read_float("Расстояние (км)", 0.01),
                    )
                    if route_id in self.routes:
                        raise ValueError("Маршрут с таким ID уже существует.")
                    self.routes[route_id] = route
                    print("Маршрут создан.")

                elif choice == "2":
                    route_id, route = self.select_from_dict(self.routes, "ID маршрута")
                    if route is None:
                        self.pause()
                        continue
                    drivers = {
                        emp_id: employee
                        for emp_id, employee
                        in self.company.employee_registry.employees.items()
                        if isinstance(employee, Driver)
                    }
                    driver_id, driver = self.select_from_dict(
                        drivers, "Табельный номер водителя"
                    )
                    if driver is None:
                        self.pause()
                        continue
                    vehicle_id, vehicle = self.select_from_dict(
                        self.company.fleet.vehicles,
                        "ID транспорта",
                    )
                    if vehicle is None:
                        self.pause()
                        continue

                    if driver.assigned_vehicle is None:
                        self.company.fleet.assign_driver(driver, vehicle_id)
                    elif driver.assigned_vehicle is not vehicle:
                        raise ValueError("Водителю уже назначен другой автомобиль.")

                    trip_id = self.read_text("ID рейса")
                    trip = Trip(trip_id, driver, vehicle, route, datetime.now())
                    if trip_id in self.trips:
                        raise ValueError("Рейс с таким ID уже существует.")
                    self.trips[trip_id] = trip
                    self.company.fleet.register_trip(trip)
                    print("Рейс создан.")

                elif choice == "3":
                    trip_id, trip = self.select_from_dict(self.trips, "ID рейса")
                    if trip is None:
                        self.pause()
                        continue
                    order_id, order = self.select_from_dict(
                        self.company.order_registry.orders,
                        "ID заказа",
                    )
                    if order is not None:
                        if order.route is None:
                            if order.origin == trip.route.origin and order.destination == trip.route.destination:
                                order.set_route(trip.route)
                        order.assign_trip(trip)
                        print("Заказ назначен на рейс.")

                elif choice == "4":
                    trip_id, trip = self.select_from_dict(self.trips, "ID рейса")
                    if trip is not None:
                        trip.start()
                        print("Рейс начат.")

                elif choice == "5":
                    trip_id, trip = self.select_from_dict(self.trips, "ID рейса")
                    if trip is not None:
                        trip.finish()
                        print("Рейс завершён. Заказы рейса отмечены доставленными.")

                elif choice == "6":
                    print("Маршруты:")
                    for route_id, route in self.routes.items():
                        print(f"{route_id}: {route.origin} → {route.destination}, {route.distance_km} км")
                    print("Рейсы:")
                    for trip_id, trip in self.trips.items():
                        print(
                            f"{trip_id}: водитель {trip.driver.name}, "
                            f"транспорт {trip.vehicle.registration_number}, статус {trip.status}"
                        )
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()

    # ---------- Финансы ----------

    def finance_menu(self):
        while True:
            self.print_header("ФИНАНСЫ")
            print("1. Выставить счёт по заказу")
            print("2. Принять оплату по счёту")
            print("3. Показать счета")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "1":
                    order_id, order = self.select_from_dict(
                        self.company.order_registry.orders,
                        "ID заказа",
                    )
                    if order is None:
                        self.pause()
                        continue
                    invoice_id = self.read_text("ID счёта")
                    invoice = Invoice(
                        invoice_id,
                        order,
                        self.read_date("Срок оплаты"),
                        self.read_float("Налоговая ставка (например 0.20)", 0),
                        self.read_float("Скидка", 0),
                    )
                    invoice.issue()
                    if invoice_id in self.invoices:
                        raise ValueError("Счёт с таким ID уже существует.")
                    self.invoices[invoice_id] = invoice
                    print(f"Счёт выставлен. Итого: {invoice.calculate_total():.2f}")

                elif choice == "2":
                    invoice_id, invoice = self.select_from_dict(self.invoices, "ID счёта")
                    if invoice is None:
                        self.pause()
                        continue
                    amount = self.read_float(
                        f"Сумма к оплате (остаток {invoice.get_balance_due():.2f})",
                        0.01,
                    )
                    payment = Payment(
                        self.read_text("ID платежа"),
                        invoice.order,
                        amount,
                        self.read_text("Способ оплаты", "bank_transfer"),
                        invoice,
                    )
                    payment.process()
                    print(f"Оплата обработана. Остаток по счёту: {invoice.get_balance_due():.2f}")

                elif choice == "3":
                    for invoice_id, invoice in self.invoices.items():
                        print(
                            f"{invoice_id}: заказ {invoice.order.order_id}, "
                            f"сумма {invoice.calculate_total():.2f}, "
                            f"оплачено {invoice.amount_paid:.2f}, статус {invoice.status}"
                        )
                elif choice == "0":
                    return
                else:
                    print("Неизвестный пункт меню.")
            except Exception as error:
                print(f"Не удалось выполнить действие: {error}")
            self.pause()

    # ---------- Главное меню ----------

    def show_summary(self):
        self.print_header("СВОДКА О КОМПАНИИ")
        for key, value in self.company.get_company_summary().items():
            print(f"{key}: {value}")
        print("\nФинансовые счета:", len(self.invoices))
        print("Маршруты:", len(self.routes))
        print("Рейсы:", len(self.trips))
        print("Грузы в каталоге:", len(self.cargos))

    def run(self):
        while True:
            self.print_header(f"СИСТЕМА УПРАВЛЕНИЯ — {self.company.name}")
            print("1. Клиенты")
            print("2. Сотрудники")
            print("3. Автопарк")
            print("4. Грузы")
            print("5. Заказы")
            print("6. Маршруты и рейсы")
            print("7. Финансы")
            print("8. Сводка по компании")
            print("0. Выход")
            choice = input("Выберите раздел: ").strip()

            if choice == "1":
                self.customers_menu()
            elif choice == "2":
                self.employees_menu()
            elif choice == "3":
                self.vehicles_menu()
            elif choice == "4":
                self.cargo_menu()
            elif choice == "5":
                self.orders_menu()
            elif choice == "6":
                self.trips_menu()
            elif choice == "7":
                self.finance_menu()
            elif choice == "8":
                self.show_summary()
                self.pause()
            elif choice == "0":
                print("Работа программы завершена.")
                return
            else:
                print("Неизвестный пункт меню.")
                self.pause()


def main():
    """Точка входа в консольное приложение."""
    try:
        ConsoleApp().run()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота программы прервана пользователем.")


if __name__ == "__main__":
    main()
