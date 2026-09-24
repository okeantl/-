"""Тесты для API эндпоинтов src/api/main.py и src/api/auth.py."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.api.main import app, products_data

# ==================== GET /products ====================


class TestGetProducts:
    def test_returns_3_products(self, client):
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_first_product_is_laptop(self, client):
        response = client.get("/products")
        assert response.json()[0]["name"] == "Ноутбук"

    def test_product_structure(self, client):
        response = client.get("/products")
        product = response.json()[0]
        assert set(product.keys()) == {"id", "name", "price", "quantity"}

    def test_all_ids_present(self, client):
        response = client.get("/products")
        ids = [p["id"] for p in response.json()]
        assert ids == [1, 2, 3]


# ==================== GET /products/{id} ====================


class TestGetProductById:
    def test_existing_product(self, client):
        response = client.get("/products/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Ноутбук"

    def test_second_product(self, client):
        response = client.get("/products/2")
        assert response.json()["name"] == "Мышь"

    def test_missing_product_returns_404(self, client):
        response = client.get("/products/999")
        assert response.status_code == 404
        assert "999" in response.json()["detail"]

    def test_negative_id_returns_404(self, client):
        response = client.get("/products/-1")
        assert response.status_code == 404

    def test_non_integer_id_returns_422(self, client):
        response = client.get("/products/abc")
        assert response.status_code == 422


# ==================== POST /products ====================


class TestCreateProduct:
    def test_create_product(self, client):
        payload = {"name": "Монитор", "price": 25000, "quantity": 5}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 4  # max(1,2,3) + 1
        assert data["name"] == "Монитор"
        assert data["price"] == 25000
        assert data["quantity"] == 5

    def test_product_added_to_catalog(self, client):
        client.post(
            "/products", json={"name": "Монитор", "price": 25000, "quantity": 5}
        )
        response = client.get("/products")
        assert len(response.json()) == 4

    @pytest.mark.parametrize(
        "bad_payload",
        [
            {"name": "", "price": 100, "quantity": 1},  # пустое имя
            {"name": "Тест", "price": 0, "quantity": 1},  # цена 0
            {"name": "Тест", "price": -100, "quantity": 1},  # отрицательная цена
            {"name": "Тест", "price": 100, "quantity": -1},  # отрицательное количество
            {"name": "Тест", "price": 100},  # нет quantity
            {"price": 100, "quantity": 1},  # нет name
        ],
    )
    def test_invalid_payloads_return_422(self, client, bad_payload):
        response = client.post("/products", json=bad_payload)
        assert response.status_code == 422

    def test_name_is_stripped(self, client):
        response = client.post(
            "/products", json={"name": "  Монитор  ", "price": 100, "quantity": 1}
        )
        assert response.json()["name"] == "Монитор"


# ==================== PUT /products/{id} ====================


class TestUpdateProduct:
    def test_update_existing(self, client):
        payload = {"name": "Ноутбук Pro", "price": 70000, "quantity": 3}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Ноутбук Pro"
        assert response.json()["price"] == 70000

    def test_update_missing_returns_404(self, client):
        payload = {"name": "X", "price": 1, "quantity": 1}
        response = client.put("/products/999", json=payload)
        assert response.status_code == 404

    def test_update_invalid_payload_returns_422(self, client):
        response = client.put(
            "/products/1", json={"name": "", "price": 100, "quantity": 1}
        )
        assert response.status_code == 422


# ==================== DELETE /products/{id} ====================


class TestDeleteProduct:
    def test_delete_existing(self, client):
        response = client.delete("/products/1")
        assert response.status_code == 204

    def test_product_removed_from_catalog(self, client):
        client.delete("/products/1")
        response = client.get("/products")
        assert len(response.json()) == 2
        ids = [p["id"] for p in response.json()]
        assert 1 not in ids

    def test_delete_missing_returns_404(self, client):
        response = client.delete("/products/999")
        assert response.status_code == 404

    def test_delete_twice_returns_404(self, client):
        assert client.delete("/products/1").status_code == 204
        assert client.delete("/products/1").status_code == 404


# ==================== POST /orders ====================


class TestCreateOrder:
    def test_create_order(self, client):
        response = client.post(
            "/orders", json={"user_id": 1, "product_id": 2, "quantity": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 5  # хардкод из main.py
        assert data["user_id"] == 1
        assert data["product_id"] == 2
        assert data["quantity"] == 1
        assert data["message"] == "Заказ создан"

    @pytest.mark.parametrize(
        "bad_payload",
        [
            {"user_id": 0, "product_id": 1, "quantity": 1},  # user_id не > 0
            {"user_id": -1, "product_id": 1, "quantity": 1},
            {"user_id": 1, "product_id": 0, "quantity": 1},  # product_id не > 0
            {"user_id": 1, "product_id": 1, "quantity": 0},  # quantity не > 0
            {"user_id": 1, "product_id": 1},  # нет quantity
            {"user_id": 1},  # нет product_id
        ],
    )
    def test_invalid_payloads_return_422(self, client, bad_payload):
        response = client.post("/orders", json=bad_payload)
        assert response.status_code == 422


# ==================== Auth: POST /register ====================


class TestRegister:
    def test_register_success(self, client):
        response = client.post(
            "/register", json={"username": "alice", "password": "pass1234"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "alice"
        assert data["id"] == 1

    def test_duplicate_username_returns_400(self, client):
        payload = {"username": "alice", "password": "pass1234"}
        client.post("/register", json=payload)
        response = client.post("/register", json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "bad_payload",
        [
            {"username": "ab", "password": "pass1234"},  # username < 3
            {"username": "alice", "password": "short"},  # password < 8
            {"username": "alice", "password": "12345678"},  # нет букв
            {"username": "alice", "password": "abcdefgh"},  # нет цифр
        ],
    )
    def test_invalid_payloads_return_422(self, client, bad_payload):
        response = client.post("/register", json=bad_payload)
        assert response.status_code == 422


# ==================== Auth: POST /login ====================


class TestLogin:
    def test_login_success(self, client):
        client.post("/register", json={"username": "alice", "password": "pass1234"})
        response = client.post(
            "/login", json={"username": "alice", "password": "pass1234"}
        )
        assert response.status_code == 200
        assert "user_id" in response.json()

    def test_wrong_password_returns_401(self, client):
        client.post("/register", json={"username": "alice", "password": "pass1234"})
        response = client.post(
            "/login", json={"username": "alice", "password": "wrongpass1"}
        )
        assert response.status_code == 401

    def test_unknown_user_returns_401(self, client):
        response = client.post(
            "/login", json={"username": "ghost", "password": "pass1234"}
        )
        assert response.status_code == 401

    def test_empty_payload_returns_422(self, client):
        response = client.post("/login", json={})
        assert response.status_code == 422


# ==================== API v1: /api/v1/products/{id} ====================
# Эти эндпоинты требуют БД (репозиторий). Проверяем только валидацию,
# а сами сервисы мокаются — глубокие тесты будут в test_services.py.


class TestApiV1Products:
    def test_missing_product_returns_404(self, client):
        with patch(
            "src.services.product_service.ProductService.get_product"
        ) as mock_get:
            from fastapi import HTTPException

            mock_get.side_effect = ValueError("Товар 999 не найден")
            response = client.get("/api/v1/products/999")
            assert response.status_code == 404

    def test_non_integer_id_returns_422(self, client):
        response = client.get("/api/v1/products/abc")
        assert response.status_code == 422


# ==================== API v1: /api/v1/orders/ ====================


class TestApiV1Orders:
    def test_create_order_missing_stock_returns_400(self, client):
        from src.services.order_service import InsufficientStockError

        with patch(
            "src.services.order_service.OrderService.create_order"
        ) as mock_create:
            mock_create.side_effect = InsufficientStockError("На складе 0 шт.")
            response = client.post(
                "/api/v1/orders/",
                json={"user_id": 1, "product_id": 1, "quantity": 5},
            )
            assert response.status_code == 400

    def test_create_order_unknown_product_returns_404(self, client):
        with patch(
            "src.services.order_service.OrderService.create_order"
        ) as mock_create:
            mock_create.side_effect = ValueError("Товар 999 не найден")
            response = client.post(
                "/api/v1/orders/",
                json={"user_id": 1, "product_id": 999, "quantity": 1},
            )
            assert response.status_code == 404


# ==================== CORS ====================


class TestCORS:
    def test_allowed_origin_header(self, client):
        response = client.get("/products", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        assert (
            response.headers.get("access-control-allow-origin")
            == "http://localhost:3000"
        )
