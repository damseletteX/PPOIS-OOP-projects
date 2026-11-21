import pytest

from library_system import Library

from .factories import make_library


@pytest.fixture
def library() -> Library:
    """Библиотека с типовым набором данных."""
    return make_library()
