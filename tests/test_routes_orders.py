"""Тесты для src/api/routes/orders.py."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.order_service import InsufficientStockError


def _mock_order():
    """Мок Order для ответа."""
    order = MagicMock()
    order.id = 1
    order.user_id = 1
    order.product_id = 2
    order.quantity = 3
    order.total = 3000.0
    order.status = "active"
    return order


class TestCreateOrderRoute:
    def test_create_success(self, client):
        order = _mock_order()
        with patch(
            "src.services.order_service.OrderService.create_order",
            new=AsyncMock(return_value=order),
        ):
            response = client.post(
                "/api/v1/orders/",
                json={"user_id": 1, "product_id": 2, "quantity": 3},
            )
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["total"] == 3000.0

    def test_create_unknown_product_returns_404(self, client):
        with patch(
            "src.services.order_service.OrderService.create_order",
            new=AsyncMock(side_effect=ValueError("Товар 999 не найден")),
        ):
            response = client.post(
                "/api/v1/orders/",
                json={"user_id": 1, "product_id": 999, "quantity": 1},
            )
        assert response.status_code == 404

    def test_create_insufficient_stock_returns_400(self, client):
        with patch(
            "src.services.order_service.OrderService.create_order",
            new=AsyncMock(side_effect=InsufficientStockError("На складе 0")),
        ):
            response = client.post(
                "/api/v1/orders/",
                json={"user_id": 1, "product_id": 1, "quantity": 5},
            )
        assert response.status_code == 400


class TestCancelOrderRoute:
    def test_cancel_success(self, client):
        order = _mock_order()
        order.status = "cancelled"
        with patch(
            "src.services.order_service.OrderService.cancel_order",
            new=AsyncMock(return_value=order),
        ):
            response = client.post("/api/v1/orders/1/cancel")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

    def test_cancel_already_cancelled_returns_400(self, client):
        with patch(
            "src.services.order_service.OrderService.cancel_order",
            new=AsyncMock(side_effect=ValueError("Заказ уже отменён")),
        ):
            response = client.post("/api/v1/orders/1/cancel")
        assert response.status_code == 400


class TestGetOrderRoute:
    def test_get_success(self, client):
        order = _mock_order()
        with patch(
            "src.services.order_service.OrderService.get_order",
            new=AsyncMock(return_value=order),
        ):
            response = client.get("/api/v1/orders/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_missing_returns_404(self, client):
        with patch(
            "src.services.order_service.OrderService.get_order",
            new=AsyncMock(return_value=None),
        ):
            response = client.get("/api/v1/orders/999")
        assert response.status_code == 404
