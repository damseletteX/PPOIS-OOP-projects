import pytest
from transport_company.application import TransportCompany
from transport_company.exceptions import DuplicateReferenceError, InvalidOrderError, CustomerNotFoundError

def test_employee_lifecycle_and_report():
    company = TransportCompany()
    employee = company.add_employee(" E1 ", "Иван", "Водитель")
    assert employee.employee_id == "E1"
    assert "Сотрудников: 1" in company.build_report()
    company.remove_employee("E1")
    assert "Сотрудников: 0" in company.build_report()

def test_employee_validation_and_duplicate():
    company = TransportCompany()
    with pytest.raises(ValueError):
        company.add_employee("", "Иван", "Водитель")
    company.add_employee("E1", "Иван", "Водитель")
    with pytest.raises(DuplicateReferenceError):
        company.add_employee("E1", "Анна", "Диспетчер")

def test_remove_unknown_employee():
    with pytest.raises(CustomerNotFoundError):
        TransportCompany().remove_employee("missing")

def test_shipment_lifecycle_and_report():
    company = TransportCompany()
    shipment = company.register_shipment("S1", "Лондон", 12.5)
    assert shipment.status == "registered"
    assert company.dispatch_shipment("S1").status == "in_transit"
    report = company.build_report()
    assert "в пути: 1" in report
    assert "12.50 кг" in report

@pytest.mark.parametrize("shipment_id,destination,weight", [
    ("", "Лондон", 1), ("S1", "", 1), ("S1", "Лондон", 0), ("S1", "Лондон", -2),
])
def test_shipment_validation(shipment_id, destination, weight):
    with pytest.raises(InvalidOrderError):
        TransportCompany().register_shipment(shipment_id, destination, weight)

def test_duplicate_shipment():
    company = TransportCompany()
    company.register_shipment("S1", "Лондон", 2)
    with pytest.raises(DuplicateReferenceError):
        company.register_shipment("S1", "Оксфорд", 3)

def test_dispatch_unknown_and_twice():
    company = TransportCompany()
    with pytest.raises(InvalidOrderError):
        company.dispatch_shipment("S1")
    company.register_shipment("S1", "Лондон", 2)
    company.dispatch_shipment("S1")
    with pytest.raises(InvalidOrderError):
        company.dispatch_shipment("S1")
