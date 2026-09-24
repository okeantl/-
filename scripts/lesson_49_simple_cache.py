import json
import time


class SimpleCache:
    """Учебная модель Redis: key-value хранилище в памяти с TTL."""

    def __init__(self):
        self._store = {}  # key -> (value, expire_at | None)

    def setex(self, key, ttl_seconds, value):
        self._store[key] = (value, time.monotonic() + ttl_seconds)

    def get(self, key):
        item = self._store.get(key)
        if item is None:
            return None
        value, expire_at = item
        if expire_at is not None and time.monotonic() >= expire_at:
            del self._store[key]
            return None
        return value

    def delete(self, key):
        self._store.pop(key, None)


# Условная "БД" SFMShop и счётчик обращений к ней
DB_PRODUCTS = [
    {"id": 1, "name": "Клавиатура", "price": 2500},
    {"id": 2, "name": "Мышь", "price": 1200},
]
db_calls = 0

cache = SimpleCache()


def get_all_products_from_db():
    global db_calls
    db_calls += 1
    return DB_PRODUCTS


def get_cached_products():
    """Кэш-aside: сначала кэш, при промахе — БД и запись в кэш."""
    cached = cache.get("products:all")
    if cached is not None:
        print("HIT")
        return json.loads(cached)
    print("MISS")
    products = get_all_products_from_db()
    cache.setex("products:all", 1, json.dumps(products))
    return products


def invalidate_products_cache():
    cache.delete("products:all")


if __name__ == "__main__":
    get_cached_products()          # MISS -> БД
    get_cached_products()          # HIT  -> кэш
    invalidate_products_cache()
    get_cached_products()          # MISS -> БД (после инвалидации)
    time.sleep(1.1)                # ждём истечения TTL
    products = get_cached_products()  # MISS -> БД (TTL истёк)
    print(f"Обращений к БД: {db_calls}")
    print(f"Товаров: {len(products)}")
