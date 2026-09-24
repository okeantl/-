import asyncio
import os

import asyncpg
from dotenv import load_dotenv

# Параметры подключения из .env — те же переменные, что в src/database/connection.py
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


class ProductRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_id(self, product_id: int) -> dict | None:
        """Получить товар по id"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, price, quantity FROM products WHERE id = $1",
                product_id
                )
            return dict(row) if row else None

    async def list_products(self, limit: int = 20, offset: int = 0) -> list[dict]:
        """Список товаров с пагинацией"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """SELECT id, name, price, quantity
                FROM products ORDER BY id LIMIT $1 OFFSET $2""",
                limit, offset
                )
            return [dict(row) for row in rows]

    async def create(self, name: str, price: float, quantity: int = 0) -> int:
        """Создать товар, вернуть id (created_at заполняет БД)"""
        async with self.pool.acquire() as conn:
            product_id = await conn.fetchval(
                """INSERT INTO products (name, price, quantity)
                VALUES ($1, $2, $3) RETURNING id""",
                name, price, quantity
                )
            return product_id

    async def update_price(self, product_id: int, new_price: float) -> bool:
        """Обновить цену товара"""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE products SET price = $1 WHERE id = $2",
                new_price, product_id
                )
            # result = "UPDATE 1" или "UPDATE 0"
            return result == "UPDATE 1"

    async def delete(self, product_id: int) -> bool:
        """Удалить товар"""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM products WHERE id = $1",
                product_id
                )
            return result == "DELETE 1"


# Использование
async def main():
    pool = await asyncpg.create_pool(**DB_CONFIG, min_size=5, max_size=10)

    repo = ProductRepository(pool)

    # Создание
    product_id = await repo.create("Тестовый товар", 1500.00, 10)
    print(f"Создан товар #{product_id}")

    # Чтение
    product = await repo.get_by_id(product_id)
    print(f"Товар: {product}")

    # Обновление
    updated = await repo.update_price(product_id, 1800.00)
    print(f"Обновлён: {updated}")

    # Список
    products = await repo.list_products(limit=5)
    print(f"Товаров: {len(products)}")

    await pool.close()

if __name__ == "__main__":
    asyncio.run(main())
