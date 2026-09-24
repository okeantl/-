import asyncio
import functools
import json

import redis.asyncio as aioredis

from src.core.config import settings

redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)


async def init_redis():
    """Проверить соединение с Redis (вызвать при старте приложения)."""
    await redis_client.ping()


def cache_async(ttl: int = 300, prefix: str = "cache"):
    """Декоратор для кэширования async-функций в Redis."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key_parts = [prefix, func.__name__, str(args), str(sorted(kwargs.items()))]
            cache_key = ":".join(key_parts)

            cached = await redis_client.get(cache_key)
            if cached is not None:
                print(f"Кэш: попадание ({cache_key})")
                return json.loads(cached)

            print(f"Кэш: промах ({cache_key})")
            result = await func(*args, **kwargs)

            await redis_client.setex(cache_key, ttl, json.dumps(result))
            return result

        return wrapper

    return decorator


@cache_async(ttl=600, prefix="products")
async def get_product(product_id: int) -> dict:
    """Получение товара из БД (кэшируется на 10 минут)."""
    await asyncio.sleep(1)
    return {"id": product_id, "name": f"Товар {product_id}", "price": 1500}


async def main():
    await init_redis()
    product = await get_product(42)
    print(f"Результат: {product}")
    product = await get_product(42)
    print(f"Результат: {product}")
    await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
