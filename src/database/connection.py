from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ

from src.core.config import settings

# Основная БД (для записи)
PRIMARY_DB = {
    "host": settings.db_primary_host,
    "port": settings.db_port,
    "database": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
}

# Реплика (для чтения)
REPLICA_DB = {
    "host": settings.db_replica_host,
    "port": settings.db_replica_port,
    "database": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
}


def connect_to_db():
    """Подключение к основной базе данных PostgreSQL."""
    return psycopg2.connect(**PRIMARY_DB)


@contextmanager
def get_connection(read_only=False):
    """Подключение к БД: основная для записи, реплика для чтения."""
    conn = psycopg2.connect(**(REPLICA_DB if read_only else PRIMARY_DB))
    try:
        yield conn
        if not read_only:
            conn.commit()
    except Exception:
        if not read_only:
            conn.rollback()
        raise
    finally:
        conn.close()


def test_connection():
    """Проверить подключение к базе данных."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"Подключение успешно! Версия PostgreSQL: {version[0]}")


def add_product(conn, name, price, quantity):
    """Добавить товар в базу данных."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
        (name, price, quantity),
    )
    conn.commit()
    cursor.close()
    print(f"Товар добавлен: {name}, {price}, {quantity}")


def get_all_products(conn):
    """Получить все товары из базы данных."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return products


def update_product_price(conn, product_id, new_price):
    """Обновить цену товара."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET price = %s WHERE id = %s",
        (new_price, product_id),
    )
    conn.commit()
    cursor.close()
    print(f"Цена обновлена: {new_price}")


if __name__ == "__main__":
    test_connection()
