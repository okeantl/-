from unittest.mock import patch
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_create_order():
    """Тест создания заказа через POST /orders"""
    # Тело запроса повторяет модель OrderCreate(user_id, product_id, quantity)
    response = client.post("/orders", json={
        "user_id": 1,
        "product_id": 2,
        "quantity": 1
        })

    # Проверка результата ровно того, что возвращает endpoint
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 5
    assert data["user_id"] == 1
    assert data["product_id"] == 2
    assert data["message"] == "Заказ создан"


@patch('src.services.cache_service.get_cached_products')
def test_get_products(mock_get_cached):
    """Тест получения товаров; кэш изолирован моком"""
    # На случай, если эндпоинт начнёт ходить в кэш — изолируем его заранее
    mock_get_cached.return_value = []

    # Вызов API
    response = client.get("/products")

    # Проверка результата
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Ноутбук"
