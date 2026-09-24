"""Общие фикстуры для всех тестов SFMShop."""

import pytest
from fastapi.testclient import TestClient

from src.api import main as api_main
from src.api.main import app, products_data
from src.models.order import Order
from src.models.product import FixedDiscount, PercentDiscount, Product
from src.models.user import User

# ---------- API ----------


@pytest.fixture
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_products_data():
    """Сбрасывает in-memory каталог товаров до исходного перед каждым тестом.

    Эндпоинты POST/PUT/DELETE меняют products_data, поэтому без сброса
    тесты влияют друг на друга.
    """
    original = [
        {"id": 1, "name": "Ноутбук", "price": 50000, "quantity": 10},
        {"id": 2, "name": "Мышь", "price": 1500, "quantity": 20},
        {"id": 3, "name": "Клавиатура", "price": 3000, "quantity": 15},
    ]
    products_data.clear()
    products_data.extend(original)
    yield
    products_data.clear()
    products_data.extend(original)


@pytest.fixture(autouse=True)
def reset_auth_users():
    """Сбрасывает in-memory users_db между тестами."""
    from src.api import auth

    auth.users_db.clear()
    yield
    auth.users_db.clear()


# ---------- Модели ----------


@pytest.fixture
def sample_product():
    """Обычный товар."""
    return Product("Ноутбук", 50000, 10)


@pytest.fixture
def sample_user():
    """Обычный пользователь."""
    return User("Иван Иванов", "ivan@example.ru")


@pytest.fixture
def sample_order(sample_user, sample_product):
    """Заказ с одним товаром."""
    return Order(user=sample_user, products=[sample_product], order_id=1)


@pytest.fixture
def sample_products():
    """Список товаров для заказа."""
    return [
        Product("Ноутбук", 50000, 1),
        Product("Мышь", 1500, 2),
        Product("Клавиатура", 3000, 1),
    ]


# ---------- Стратегии скидок ----------


@pytest.fixture
def percent_discount():
    return PercentDiscount(percent=10)


@pytest.fixture
def fixed_discount():
    return FixedDiscount(amount=500)


# ---------- Моки внешних сервисов ----------


@pytest.fixture
def mock_redis(mocker):
    """Мок Redis-клиента (синхронного)."""
    fake = mocker.MagicMock()
    fake.get.return_value = None
    return fake
