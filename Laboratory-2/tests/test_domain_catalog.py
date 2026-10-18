import inspect
import pytest
import transport_company as domain

VALUE_BY_NAME = {
    "str": "test", "int": 1, "float": 1.0, "bool": True,
    "Optional[str]": None, "Optional[float]": None, "Optional[int]": None,
}

def argument_value(parameter):
    annotation = str(parameter.annotation)
    name = parameter.name.lower()
    if "status" in name:
        return "draft"
    if "date" in name or "time" in name:
        return "2026-10-18"
    if "email" in name:
        return "test@example.com"
    if "phone" in name:
        return "+441234567890"
    if "weight" in name or "volume" in name or "capacity" in name or "amount" in name or "price" in name or "cost" in name:
        return 1.0
    if "quantity" in name or "count" in name or "days" in name or "number" in name:
        return 1
    if "enabled" in name or "active" in name or "opt_in" in name:
        return True
    if "optional" in annotation.lower() or "none" in annotation.lower():
        return None
    if parameter.default is not inspect.Parameter.empty:
        return parameter.default
    if annotation in VALUE_BY_NAME:
        return VALUE_BY_NAME[annotation]
    return "test"

def domain_classes():
    excluded = (BaseException, type)
    for _, value in inspect.getmembers(domain, inspect.isclass):
        if value.__module__.startswith("transport_company.") and not issubclass(value, excluded):
            if value.__name__.endswith("Error"):
                continue
            if value.__name__ not in {"TransportCompany"}:
                yield value

@pytest.mark.parametrize("entity_class", list(domain_classes()), ids=lambda cls: cls.__name__)
def test_domain_entity_constructs(entity_class):
    signature = inspect.signature(entity_class)
    kwargs = {
        name: argument_value(parameter)
        for name, parameter in signature.parameters.items()
        if name != "self" and parameter.kind in (parameter.POSITIONAL_OR_KEYWORD, parameter.KEYWORD_ONLY)
    }
    entity = entity_class(**kwargs)
    assert entity is not None

def method_cases():
    cases = []
    for entity_class in domain_classes():
        for name, method in inspect.getmembers(entity_class, inspect.isfunction):
            if name.startswith("_") or name == "__init__":
                continue
            cases.append((entity_class, name, method))
    return cases

@pytest.mark.parametrize("entity_class,method_name,method", method_cases(),
                         ids=lambda item: getattr(item, "__name__", str(item)))
def test_domain_methods_execute(entity_class, method_name, method):
    signature = inspect.signature(entity_class)
    kwargs = {
        name: argument_value(parameter)
        for name, parameter in signature.parameters.items()
        if name != "self" and parameter.kind in (parameter.POSITIONAL_OR_KEYWORD, parameter.KEYWORD_ONLY)
    }
    entity = entity_class(**kwargs)
    result = getattr(entity, method_name)()
    assert result is not None
    assert isinstance(result, (str, int, float, bool, tuple, list, dict))
