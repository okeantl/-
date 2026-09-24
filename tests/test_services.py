"""Тесты для src/services/."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.exchange_client import ExchangeClient
from src.services.order_service import InsufficientStockError, OrderService

# ==================== ExchangeClient ====================


class TestExchangeClient:
    @patch("src.services.exchange_client.requests.get")
    def test_get_exchange_rate(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"RUB": 92.5, "EUR": 0.92}}
        mock_get.return_value = mock_response

        rate = ExchangeClient().get_exchange_rate("USD", "RUB")

        assert rate == 92.5
        mock_get.assert_called_once_with(
            "https://api.exchangerate-api.com/v4/latest/USD",
            timeout=5,
        )

    @patch("src.services.exchange_client.requests.get")
    def test_get_exchange_rate_unknown_currency(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.92}}
        mock_get.return_value = mock_response

        assert ExchangeClient().get_exchange_rate("USD", "XYZ") is None

    @patch("src.services.exchange_client.requests.get")
    def test_custom_base_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"RUB": 100.0}}
        mock_get.return_value = mock_response

        client = ExchangeClient(base_url="https://custom.api/v1")
        rate = client.get_exchange_rate("USD", "RUB")

        assert rate == 100.0
        mock_get.assert_called_once_with(
            "https://custom.api/v1/USD",
            timeout=5,
        )

    @patch("src.services.exchange_client.requests.get")
    def test_request_exception_returns_none(self, mock_get):
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException("connection error")

        assert ExchangeClient().get_exchange_rate("USD", "RUB") is None

    @patch("src.services.exchange_client.requests.get")
    def test_timeout_returns_none_after_retries(self, mock_get):
        from requests.exceptions import Timeout

        mock_get.side_effect = Timeout("timed out")

        # Патчим time.sleep, чтобы не ждать реальные 1+2 секунды
        with patch("src.services.exchange_client.time.sleep"):
            rate = ExchangeClient().get_exchange_rate("USD", "RUB")

        assert rate is None
        # 3 попытки по max_retries
        assert mock_get.call_count == 3


# ==================== OrderService ====================


def _make_product(price=1000, quantity=10):
    """Мок ORM-товара."""
    p = MagicMock()
    p.price = price
    p.quantity = quantity
    return p


def _make_order_repo(order=None):
    repo = MagicMock()
    repo.create = AsyncMock(return_value=order)
    repo.get_by_id = AsyncMock(return_value=order)
    return repo


def _make_product_repo(product=None):
    repo = MagicMock()
    repo.get_by_id = AsyncMock(return_value=product)
    repo.update_stock = AsyncMock()
    return repo


class TestOrderServiceCreateOrder:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        product = _make_product(price=1000, quantity=10)
        order = MagicMock()
        order_repo = _make_order_repo(order)
        product_repo = _make_product_repo(product)
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        result = await service.create_order(user_id=1, product_id=1, quantity=2)

        assert result is order
        order_repo.create.assert_awaited_once()
        product_repo.update_stock.assert_awaited_once_with(1, -2)

    @pytest.mark.asyncio
    async def test_create_order_unknown_product(self):
        order_repo = _make_order_repo()
        product_repo = _make_product_repo(product=None)
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        with pytest.raises(ValueError, match="не найден"):
            await service.create_order(user_id=1, product_id=999, quantity=1)

        order_repo.create.assert_not_called()
        product_repo.update_stock.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        product = _make_product(price=1000, quantity=2)
        order_repo = _make_order_repo()
        product_repo = _make_product_repo(product)
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        with pytest.raises(InsufficientStockError):
            await service.create_order(user_id=1, product_id=1, quantity=5)

        order_repo.create.assert_not_called()
        product_repo.update_stock.assert_not_called()

    @pytest.mark.asyncio
    async def test_bulk_discount_applied(self):
        """При quantity >= 10 применяется скидка 10%."""
        product = _make_product(price=1000, quantity=100)
        captured = {}

        async def fake_create(order):
            captured["order"] = order
            return order

        order_repo = MagicMock()
        order_repo.create = AsyncMock(side_effect=fake_create)
        product_repo = _make_product_repo(product)
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        await service.create_order(user_id=1, product_id=1, quantity=10)

        # 1000 * 10 * 0.9 = 9000
        assert captured["order"].total == 9000

    @pytest.mark.asyncio
    async def test_no_bulk_discount_below_threshold(self):
        product = _make_product(price=1000, quantity=100)
        captured = {}

        async def fake_create(order):
            captured["order"] = order
            return order

        order_repo = MagicMock()
        order_repo.create = AsyncMock(side_effect=fake_create)
        product_repo = _make_product_repo(product)
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        await service.create_order(user_id=1, product_id=1, quantity=9)

        # 1000 * 9 = 9000, без скидки
        assert captured["order"].total == 9000


class TestOrderServiceCancelOrder:
    @pytest.mark.asyncio
    async def test_cancel_order_success(self):
        order = MagicMock()
        order.status = "active"
        order.product_id = 1
        order.quantity = 3
        order_repo = _make_order_repo(order)
        product_repo = _make_product_repo()
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        result = await service.cancel_order(order_id=1)

        assert result.status == "cancelled"
        product_repo.update_stock.assert_awaited_once_with(1, 3)

    @pytest.mark.asyncio
    async def test_cancel_unknown_order(self):
        order_repo = _make_order_repo(order=None)
        product_repo = _make_product_repo()
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        with pytest.raises(ValueError, match="не найден"):
            await service.cancel_order(order_id=999)

    @pytest.mark.asyncio
    async def test_cancel_already_cancelled(self):
        order = MagicMock()
        order.status = "cancelled"
        order_repo = _make_order_repo(order)
        product_repo = _make_product_repo()
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        with pytest.raises(ValueError, match="уже отменён"):
            await service.cancel_order(order_id=1)


class TestOrderServiceGetOrder:
    @pytest.mark.asyncio
    async def test_get_order(self):
        order = MagicMock()
        order_repo = _make_order_repo(order)
        product_repo = _make_product_repo()
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        assert await service.get_order(1) is order

    @pytest.mark.asyncio
    async def test_get_unknown_order_returns_none(self):
        order_repo = _make_order_repo(order=None)
        product_repo = _make_product_repo()
        service = OrderService(order_repo=order_repo, product_repo=product_repo)

        assert await service.get_order(999) is None


# ==================== _calculate_total ====================


class TestOrderServiceCalculateTotal:
    def _service(self):
        return OrderService(order_repo=MagicMock(), product_repo=MagicMock())

    @pytest.mark.parametrize(
        "price,quantity,expected",
        [
            (100, 1, 100),
            (100, 5, 500),
            (100, 9, 900),  # без скидки
            (100, 10, 900),  # 1000 * 0.9
            (100, 20, 1800),  # 2000 * 0.9
            (50, 10, 450),  # 500 * 0.9
        ],
    )
    def test_calculate_total(self, price, quantity, expected):
        service = self._service()
        assert service._calculate_total(price, quantity) == expected

    def test_decimal_price_converted_to_float(self):
        from decimal import Decimal

        service = self._service()
        result = service._calculate_total(Decimal("100.50"), 2)
        assert result == 201.0


# ==================== cache_service ====================


class TestCacheService:
    @patch("src.services.cache_service.redis_client")
    @patch("src.services.cache_service.get_all_products_from_db")
    def test_cache_miss_fetches_from_db(self, mock_db, mock_redis):
        import json

        mock_redis.get.return_value = None
        mock_db.return_value = [{"id": 1, "name": "Ноутбук"}]

        from src.services.cache_service import get_cached_products

        result = get_cached_products()

        assert result == [{"id": 1, "name": "Ноутбук"}]
        mock_db.assert_called_once()
        mock_redis.setex.assert_called_once()
        # Проверяем, что в setex передан JSON
        args = mock_redis.setex.call_args[0]
        assert args[0] == "products:all"
        assert args[1] == 3600
        assert json.loads(args[2]) == [{"id": 1, "name": "Ноутбук"}]

    @patch("src.services.cache_service.redis_client")
    @patch("src.services.cache_service.get_all_products_from_db")
    def test_cache_hit_does_not_touch_db(self, mock_db, mock_redis):
        import json

        mock_redis.get.return_value = json.dumps([{"id": 1, "name": "Из кэша"}])

        from src.services.cache_service import get_cached_products

        result = get_cached_products()

        assert result == [{"id": 1, "name": "Из кэша"}]
        mock_db.assert_not_called()

    @patch("src.services.cache_service.redis_client")
    def test_invalidate_cache(self, mock_redis):
        from src.services.cache_service import invalidate_products_cache

        invalidate_products_cache()
        mock_redis.delete.assert_called_once_with("products:all")


class TestExchangeClientRetry:
    @patch("src.services.exchange_client.requests.get")
    def test_connection_error_retries_3_times(self, mock_get):
        from requests.exceptions import ConnectionError as ReqConnErr

        mock_get.side_effect = ReqConnErr("no route")
        with patch("src.services.exchange_client.time.sleep"):
            rate = ExchangeClient().get_exchange_rate("USD", "RUB")
        assert rate is None
        assert mock_get.call_count == 3

    @patch("src.services.exchange_client.requests.get")
    def test_success_after_one_timeout(self, mock_get):
        from requests.exceptions import Timeout

        good = MagicMock()
        good.json.return_value = {"rates": {"RUB": 90.0}}
        mock_get.side_effect = [Timeout("slow"), good]
        with patch("src.services.exchange_client.time.sleep"):
            rate = ExchangeClient().get_exchange_rate("USD", "RUB")
        assert rate == 90.0
        assert mock_get.call_count == 2
