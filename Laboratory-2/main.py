"""Console interface; business operations live in transport_company.application."""
from transport_company.application import TransportCompany

def main() -> None:
    company = TransportCompany()
    actions = {
        "1": lambda: add_employee(company),
        "2": lambda: remove_employee(company),
        "3": lambda: register_shipment(company),
        "4": lambda: dispatch_shipment(company),
        "5": lambda: print(company.build_report()),
    }
    while True:
        print("\nТранспортная компания")
        print("1. Добавить сотрудника")
        print("2. Удалить сотрудника")
        print("3. Зарегистрировать отправление")
        print("4. Отправить посылку")
        print("5. Сформировать отчёт")
        print("0. Выход")
        choice = input("> ").strip()
        if choice == "0":
            return
        action = actions.get(choice)
        if action is None:
            print("Неизвестный пункт меню.")
            continue
        try:
            action()
        except (ValueError, RuntimeError) as error:
            print(f"Ошибка: {error}")
        except Exception as error:
            print(f"Операция не выполнена: {error}")

def add_employee(company) -> None:
    employee_id = input("ID сотрудника: ")
    name = input("Имя: ")
    role = input("Должность: ")
    print("Добавлен:", company.add_employee(employee_id, name, role))

def remove_employee(company) -> None:
    company.remove_employee(input("ID сотрудника: ").strip())
    print("Сотрудник удалён.")

def register_shipment(company) -> None:
    shipment_id = input("Номер отправления: ")
    destination = input("Адрес назначения: ")
    weight = float(input("Вес, кг: "))
    print("Зарегистрировано:", company.register_shipment(shipment_id, destination, weight))

def dispatch_shipment(company) -> None:
    shipment = company.dispatch_shipment(input("Номер отправления: ").strip())
    print("Отправление передано в перевозку:", shipment.shipment_id)

if __name__ == "__main__":
    main()
