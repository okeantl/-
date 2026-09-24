import json

import redis

from src.core.config import settings
from src.database.queries import get_all_products_from_db

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def get_cached_products():
    """Получение товаров с кэшированием в Redis."""
    cache_key = "products:all"

    cached = redis_client.get(cache_key)
    if cached:
        print("Данные из кэша Redis")
        return json.loads(cached)

    print("Данные из PostgreSQL")
    products = get_all_products_from_db()

    redis_client.setex(cache_key, 3600, json.dumps(products))
    return products


def invalidate_products_cache():
    """Инвалидация кэша товаров."""
    redis_client.delete("products:all")
    print("Кэш товаров очищен")


if __name__ == "__main__":
    products1 = get_cached_products()
    products2 = get_cached_products()
    invalidate_products_cache()
