"""Тесты для src/repositories/ через мок AsyncSession."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository


def _session():
    session = MagicMock()
    session.execute = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    return session


class TestOrderRepository:
    @pytest.mark.asyncio
    async def test_get_by_id_found(self):
        session = _session()
        order = MagicMock()
        result = MagicMock()
        result.scalar_one_or_none.return_value = order
        session.execute.return_value = result

        repo = OrderRepository(session)
        assert await repo.get_by_id(1) is order

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self):
        session = _session()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        session.execute.return_value = result

        repo = OrderRepository(session)
        assert await repo.get_by_id(999) is None

    @pytest.mark.asyncio
    async def test_create(self):
        session = _session()
        order = MagicMock()

        repo = OrderRepository(session)
        result = await repo.create(order)

        session.add.assert_called_once_with(order)
        session.flush.assert_awaited_once()
        assert result is order


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_get_by_id_found(self):
        session = _session()
        product = MagicMock()
        result = MagicMock()
        result.scalar_one_or_none.return_value = product
        session.execute.return_value = result

        repo = ProductRepository(session)
        assert await repo.get_by_id(1) is product

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self):
        session = _session()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        session.execute.return_value = result

        repo = ProductRepository(session)
        assert await repo.get_by_id(999) is None

    @pytest.mark.asyncio
    async def test_get_all(self):
        session = _session()
        products = [MagicMock(), MagicMock()]
        result = MagicMock()
        result.scalars.return_value.all.return_value = products
        session.execute.return_value = result

        repo = ProductRepository(session)
        assert await repo.get_all(skip=0, limit=10) == products

    @pytest.mark.asyncio
    async def test_create(self):
        session = _session()
        product = MagicMock()

        repo = ProductRepository(session)
        result = await repo.create(product)

        session.add.assert_called_once_with(product)
        session.flush.assert_awaited_once()
        assert result is product

    @pytest.mark.asyncio
    async def test_update_stock(self):
        session = _session()
        product = MagicMock()
        product.quantity = 10

        repo = ProductRepository(session)
        # Мокаем get_by_id, чтобы вернуть product
        repo.get_by_id = AsyncMock(return_value=product)

        await repo.update_stock(1, -3)

        assert product.quantity == 7

    @pytest.mark.asyncio
    async def test_update_stock_missing_product(self):
        session = _session()
        repo = ProductRepository(session)
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ValueError, match="не найден"):
            await repo.update_stock(999, -1)

    @pytest.mark.asyncio
    async def test_search_no_filters(self):
        session = _session()
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        session.execute.return_value = result

        repo = ProductRepository(session)
        result = await repo.search()
        assert result == []

    @pytest.mark.asyncio
    async def test_search_with_filters(self):
        session = _session()
        products = [MagicMock()]
        result = MagicMock()
        result.scalars.return_value.all.return_value = products
        session.execute.return_value = result

        repo = ProductRepository(session)
        found = await repo.search(name_query="Ноут", min_price=100, max_price=9999)
        assert found == products
        session.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_search_only_name(self):
        session = _session()
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        session.execute.return_value = result

        repo = ProductRepository(session)
        await repo.search(name_query="X")
        session.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_search_only_min_price(self):
        session = _session()
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        session.execute.return_value = result

        repo = ProductRepository(session)
        await repo.search(min_price=100)
        session.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_search_only_max_price(self):
        session = _session()
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        session.execute.return_value = result

        repo = ProductRepository(session)
        await repo.search(max_price=1000)
        session.execute.assert_awaited_once()


# ==================== database/models.get_session ====================


class TestGetSession:
    def test_returns_session(self):
        from src.database.models import SessionLocal, get_session

        session = get_session()
        assert session is not None
        session.close()
