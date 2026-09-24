from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.services.order_service import OrderService
from src.services.product_service import ProductService

ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

from sqlalchemy.ext.asyncio import async_sessionmaker

engine = create_async_engine(ASYNC_DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Сессия БД с автоматическим закрытием."""
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_product_repository(
    session: AsyncSession = Depends(get_session),
) -> ProductRepository:
    """Репозиторий товаров."""
    return ProductRepository(session)


async def get_order_repository(
    session: AsyncSession = Depends(get_session),
) -> OrderRepository:
    """Репозиторий заказов."""
    return OrderRepository(session)


async def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
) -> OrderService:
    """Сервис заказов со всеми зависимостями."""
    return OrderService(order_repo=order_repo, product_repo=product_repo)


async def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    return ProductService(product_repo=product_repo)
