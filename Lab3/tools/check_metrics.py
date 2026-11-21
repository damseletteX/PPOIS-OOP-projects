"""Проверка количественных и стилевых требований к проекту.

Запуск из корня репозитория: python tools/check_metrics.py
"""

import ast
import sys
from pathlib import Path

DOMAIN_ROOT = Path("library_system")
CHECKED_ROOTS = (DOMAIN_ROOT, Path("cli"), Path("tools"), Path("tests"), Path("main.py"))
EXCEPTIONS_DIR = "exceptions"
TESTS_DIR = "tests"
ENUM_BASES = {"Enum"}
TODO_MARKER = "TODO"
MAX_METHOD_LINES = 20
MAX_LINE_LENGTH = 150
MAX_NESTING = 3
ALLOWED_NUMBERS = {0, 1, -1}
BANNED_NAMES = {
    "temp",
    "tmp",
    "k",
    "p",
    "buffer",
    "help",
    "data",
    "x",
    "y",
    "i",
    "j",
    "r",
    "c",
    "b",
    "s",
}
NESTING_NODES = (ast.If, ast.For, ast.While, ast.Try, ast.With)
REQUIREMENTS = {
    "classes": 50,
    "fields": 150,
    "behaviors": 100,
    "associations": 30,
    "exceptions": 12,
}


def python_files(root: Path) -> list[Path]:
    """Возвращает все .py-файлы под указанным путём."""
    if root.is_file():
        return [root]
    return sorted(root.rglob("*.py")) if root.exists() else []


def parse(path: Path) -> ast.Module:
    """Разбирает файл в дерево синтаксиса."""
    return ast.parse(path.read_text(encoding="utf-8"))


def base_names(node: ast.ClassDef) -> set[str]:
    """Возвращает имена базовых классов."""
    names = set()
    for base in node.bases:
        names.add(base.id if isinstance(base, ast.Name) else getattr(base, "attr", ""))
    return names


def classify(node: ast.ClassDef, path: Path) -> str:
    """Определяет группу класса: перечисление, исключение или доменный класс."""
    if base_names(node) & ENUM_BASES:
        return "enums"
    return "exceptions" if EXCEPTIONS_DIR in path.parts else "domain"


def collect_classes() -> dict[str, list[ast.ClassDef]]:
    """Делит классы пакета на доменные, исключения и перечисления."""
    groups = {"domain": [], "exceptions": [], "enums": []}
    for path in python_files(DOMAIN_ROOT):
        classes = [node for node in parse(path).body if isinstance(node, ast.ClassDef)]
        for node in classes:
            groups[classify(node, path)].append(node)
    return groups


def methods_of(node: ast.ClassDef) -> list[ast.FunctionDef]:
    """Возвращает методы класса."""
    return [item for item in node.body if isinstance(item, ast.FunctionDef)]


def assigned_attributes(method: ast.FunctionDef) -> set[str]:
    """Возвращает имена атрибутов self, которым что-то присваивается в методе."""
    names = set()
    for child in ast.walk(method):
        targets = (
            child.targets if isinstance(child, ast.Assign) else [getattr(child, "target", None)]
        )
        names |= {target.attr for target in targets if is_self_attribute(target)}
    return names


def is_self_attribute(target: ast.AST | None) -> bool:
    """Проверяет, что узел имеет вид self.имя."""
    return isinstance(target, ast.Attribute) and getattr(target.value, "id", "") == "self"


def self_fields(node: ast.ClassDef) -> set[str]:
    """Возвращает имена полей, присваиваемых через self."""
    fields = set()
    for method in methods_of(node):
        fields |= assigned_attributes(method)
    return fields


def is_trivial(method: ast.FunctionDef) -> bool:
    """Проверяет, что метод — геттер или сеттер без логики."""
    body = [item for item in method.body if not isinstance(item, ast.Expr)]
    if len(body) != 1:
        return False
    statement = body[0]
    if isinstance(statement, ast.Return):
        return isinstance(statement.value, ast.Attribute)
    return isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Name)


def behaviors(domain: list[ast.ClassDef]) -> list[tuple[str, str]]:
    """Возвращает пары (класс, метод) содержательных поведений."""
    found = []
    for node in domain:
        for method in methods_of(node):
            if not method.name.startswith("__") and not is_trivial(method):
                found.append((node.name, method.name))
    return found


def annotation_names(node: ast.AST) -> set[str]:
    """Собирает имена классов из аннотации."""
    return {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}


def method_annotations(method: ast.FunctionDef) -> list[ast.AST]:
    """Возвращает аннотации параметров метода и аннотированных присваиваний."""
    annotations = [arg.annotation for arg in method.args.args if arg.annotation]
    annotated = [child for child in ast.walk(method) if isinstance(child, ast.AnnAssign)]
    return annotations + [child.annotation for child in annotated]


def class_associations(node: ast.ClassDef, class_names: set[str]) -> set[tuple[str, str]]:
    """Возвращает пары (класс, связанный класс) для одного класса."""
    used = set()
    for method in methods_of(node):
        for annotation in method_annotations(method):
            used |= annotation_names(annotation)
    return {(node.name, name) for name in used & class_names - {node.name}}


def associations(domain: list[ast.ClassDef]) -> set[tuple[str, str]]:
    """Находит пары классов, где один встречается в аннотациях полей или параметров другого."""
    class_names = {node.name for node in domain}
    pairs = set()
    for node in domain:
        pairs |= class_associations(node, class_names)
    return pairs


def nesting_depth(node: ast.AST, depth: int = 0) -> int:
    """Возвращает максимальную вложенность ветвлений и циклов."""
    deepest = depth
    for child in ast.iter_child_nodes(node):
        is_nesting = isinstance(child, NESTING_NODES)
        deepest = max(deepest, nesting_depth(child, depth + (1 if is_nesting else 0)))
    return deepest


def style_issues(path: Path) -> list[str]:
    """Проверяет длину строк, методов, вложенность, имена и магические числа."""
    issues = []
    source = path.read_text(encoding="utf-8")
    is_self = path.resolve() == Path(__file__).resolve()
    for number, line in enumerate(source.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH:
            issues.append(f"{path}:{number}: строка длиннее {MAX_LINE_LENGTH}")
        if TODO_MARKER in line and not is_self:
            issues.append(f"{path}:{number}: {TODO_MARKER}")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        issues += node_issues(path, node)
    return issues


def node_issues(path: Path, node: ast.AST) -> list[str]:
    """Проверяет отдельный узел дерева."""
    issues = []
    if isinstance(node, ast.FunctionDef):
        length = node.end_lineno - node.lineno + 1
        if length > MAX_METHOD_LINES:
            issues.append(
                f"{path}:{node.lineno}: {node.name} длиннее {MAX_METHOD_LINES} строк ({length})"
            )
        if nesting_depth(node) > MAX_NESTING:
            issues.append(f"{path}:{node.lineno}: {node.name} вложенность больше {MAX_NESTING}")
        if TESTS_DIR not in path.parts:
            issues += number_issues(path, node)
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in BANNED_NAMES:
        issues.append(f"{path}:{node.lineno}: неинформативное имя {node.id}")
    if isinstance(node, ast.arg) and node.arg in BANNED_NAMES:
        issues.append(f"{path}:{node.lineno}: неинформативное имя {node.arg}")
    return issues


def number_issues(path: Path, function: ast.FunctionDef) -> list[str]:
    """Ищет числовые литералы-«магические числа» в теле функции."""
    issues = []
    for child in ast.walk(function):
        is_number = isinstance(child, ast.Constant) and isinstance(child.value, (int, float))
        if is_number and not isinstance(child.value, bool) and child.value not in ALLOWED_NUMBERS:
            issues.append(f"{path}:{child.lineno}: магическое число {child.value}")
    return issues


def report_counts(groups: dict[str, list[ast.ClassDef]]) -> dict[str, int]:
    """Считает показатели по требованиям задания."""
    domain = groups["domain"]
    behavior_list = behaviors(domain)
    return {
        "classes": len(domain),
        "fields": sum(len(self_fields(node)) for node in domain),
        "behaviors": len({name for _, name in behavior_list}),
        "associations": len(associations(domain)),
        "exceptions": len(groups["exceptions"]),
    }


def main() -> int:
    """Печатает отчёт и возвращает код возврата (0 — все требования выполнены)."""
    counts = report_counts(collect_classes())
    failed = False
    for name, required in REQUIREMENTS.items():
        status = "OK " if counts[name] >= required else "FAIL"
        failed = failed or counts[name] < required
        print(f"[{status}] {name}: {counts[name]} (нужно не менее {required})")
    issues = [
        issue
        for root in CHECKED_ROOTS
        for path in python_files(root)
        for issue in style_issues(path)
    ]
    print("\n".join(issues) if issues else "Стилевых замечаний нет.")
    return 1 if failed or issues else 0


if __name__ == "__main__":
    sys.exit(main())
