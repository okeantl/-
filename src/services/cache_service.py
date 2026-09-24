import json
import redis
from src.database.queries import get_all_products_from_db

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cached_products():
    """Получение товаров с кэшированием в Redis"""
    cache_key = "products:all"

    # Проверка кэша
    cached = redis_client.get(cache_key)
    if cached:
        print("Данные из кэша Redis")
        return json.loads(cached)

    # Данных нет в кэше - получаем из БД
    print("Данные из PostgreSQL")
    products = get_all_products_from_db()

    # Сохраняем в кэш на 1 час (3600 секунд)
    redis_client.setex(cache_key, 3600, json.dumps(products))

    return products

def invalidate_products_cache():
    """Инвалидация кэша товаров"""
    redis_client.delete("products:all")
    print("Кэш товаров очищен")

# Тестирование
if __name__ == "__main__":
    # Первый запрос - из БД
    products1 = get_cached_products()

    # Второй запрос - из кэша
    products2 = get_cached_products()

    # Инвалидация кэша
    invalidate_products_cache()
