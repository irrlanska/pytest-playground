import pytest
import requests

# ========== Фикстуры для API-тестов (новые) ==========

# Константа с адресом тестируемого сервера.
# Если сервер переедет, достаточно изменить эту строку.
BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_session():
    """
    Создаёт HTTP-сессию, которая живёт всё время выполнения тестов.

    Сессия переиспользует TCP-соединение, что ускоряет тесты.
    scope="session" — держит одно соединение для всех тестов
    """
    session = requests.Session()   # создаём сессию
    yield session                  # отдаём её тестам
    session.close()                # после всех тестов закрываем соединение


@pytest.fixture
def api_url():
    """
    Возвращает базовый URL тестируемого API.

    Пока это просто константа, но в будущем URL можно будет
    передавать из командной строки или переменных окружения.
    """
    return BASE_URL

@pytest.fixture
def empty_cart():
    return []


@pytest.fixture
def single_apple():
    return [{"name": "apple", "price": 10, "quantity": 1}]

@pytest.fixture
def cart_with_items():
    return [
        {"name": "apple", "price": 10, "quantity": 1},
        {"name": "banana", "price": 20, "quantity": 1},
    ]

@pytest.fixture
def cart_with_discounts():
    return [
        {"name": "apple", "price": 10, "discount": 20, "quantity": 1},
        {"name": "banana", "price": 20, "discount": 0, "quantity": 1},
        {"name": "orange", "price": 30, "discount": 100, "quantity": 1},
    ]

@pytest.fixture
def big_cart():
    return [{"name": f"item_{i}", "price": 10, "quantity": 1} for i in range(1000)]

@pytest.fixture
def huge_cart():
    return [{"name": f"item_{i}", "price": 10, "quantity": 1} for i in range(100_000)]

@pytest.fixture
def fractional_cart():
    return [{"name": "banana", "price": 100, "quantity": 0.3}]


@pytest.fixture
def max_cart():
    return [{"name": f"item_{i}", "price": 1, "quantity": 1} for i in range(50)]


@pytest.fixture
def overpriced_cart():
    return [{"name": "expensive", "price": 1_000_001, "quantity": 1}]


@pytest.fixture
def xss_cart():
    return [{"name": "<script>alert('xss')</script>", "price": 10, "quantity": 1}]


@pytest.fixture
def sql_injection_cart():
    return [{"name": "apple'; DROP TABLE cart;--", "price": 10, "quantity": 1}]


@pytest.fixture
def long_name_cart():
    return [{"name": "a" * 10000, "price": 10, "quantity": 1}]


@pytest.fixture
def null_cart():
    return [None]


@pytest.fixture
def mixed_currency_cart():
    return [
        {"name": "apple", "price": 10, "currency": "USD", "quantity": 1},
        {"name": "banana", "price": 20, "currency": "EUR", "quantity": 1},
    ]


@pytest.fixture
def single_currency_cart():
    return [
        {"name": "apple", "price": 10, "currency": "USD", "quantity": 1},
        {"name": "banana", "price": 20, "currency": "USD", "quantity": 1},
    ]