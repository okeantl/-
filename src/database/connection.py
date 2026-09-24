import os
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Параметры подключения из переменных окружения (пароль не хранится в коде)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

# Основная БД (для записи)
PRIMARY_DB = {
    "host": os.getenv("DB_PRIMARY_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

# Реплика (для чтения)
REPLICA_DB = {
    "host": os.getenv("DB_REPLICA_HOST", "localhost"),
    "port": int(os.getenv("DB_REPLICA_PORT", 5433)),
    "database": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def connect_to_db():
    """Подключение к базе данных PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)


@contextmanager
def get_connection(read_only=False):
    """Получить подключение к БД (основная для записи или реплика для чтения)."""
    if read_only:
        # Чтение из реплики
        conn = psycopg2.connect(**REPLICA_DB)
    else:
        # Запись в основную БД
        conn = psycopg2.connect(**PRIMARY_DB)

    try:
        yield conn
        if not read_only:
            conn.commit()
    except Exception as e:
        if not read_only:
            conn.rollback()
        raise
    finally:
        conn.close()


def test_connection():
    """Проверить подключение к базе данных"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"Подключение успешно! Версия PostgreSQL: {version[0]}")


def add_product(conn, name, price, quantity):
    """Добавить товар в базу данных"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
        (name, price, quantity)
        )
    conn.commit()
    cursor.close()
    print(f"Товар добавлен: {name}, {price}, {quantity}")


def get_all_products(conn):
    """Получить все товары из базы данных"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return products


def update_product_price(conn, product_id, new_price):
    """Обновить цену товара"""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET price = %s WHERE id = %s",
        (new_price, product_id)
        )
    conn.commit()
    cursor.close()
    print(f"Цена обновлена: {new_price}")


def main():
    # Подключение к БД
    conn = connect_to_db()

    try:
        # Добавить товар
        add_product(conn, "Ноутбук", 50000.00, 10)

        # Получить все товары
        products = get_all_products(conn)
        print("Все товары:")
        for product in products:
            print(product)

        # Обновить цену
        update_product_price(conn, 1, 45000.00)

    finally:
        conn.close()


if __name__ == "__main__":
    test_connection()
