"""Тесты для src/services/product_service.py."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.services.product_service import ProductService


def _service(product=None):
    repo = MagicMock()
    repo.get_by_id = AsyncMock(return_value=product)
    repo.search = AsyncMock(return_value=[])
    return ProductService(product_repo=repo), repo


class TestGetProduct:
    @pytest.mark.asyncio
    async def test_get_existing(self):
        product = MagicMock()
        service, _ = _service(product)
        assert await service.get_product(1) is product

    @pytest.mark.asyncio
    async def test_get_missing_raises(self):
        service, _ = _service(product=None)
        with pytest.raises(ValueError, match="не найден"):
            await service.get_product(999)


class TestSearchProducts:
    @pytest.mark.asyncio
    async def test_search_no_filters(self):
        service, repo = _service()
        await service.search_products()
        repo.search.assert_awaited_once_with(
            name_query=None, min_price=None, max_price=None
        )

    @pytest.mark.asyncio
    async def test_search_with_filters(self):
        service, repo = _service()
        await service.search_products(name_query="Ноут", min_price=1000, max_price=5000)
        repo.search.assert_awaited_once_with(
            name_query="Ноут", min_price=1000, max_price=5000
        )
