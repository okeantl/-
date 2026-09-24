import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ
from src.database.connection import get_connection

def get_orders_with_products(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
        orders.id,
        products.name,
        order_items.quantity,
        products.price
        FROM orders
        INNER JOIN order_items ON orders.id = order_items.order_id
        INNER JOIN products ON order_items.product_id = products.id
        WHERE orders.user_id = %s
        """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    return results

def get_order_statistics(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, COUNT(*) as order_count, SUM(total) as total_sum
        FROM orders
        GROUP BY user_id
        ORDER BY total_sum DESC
        """)
    results = cursor.fetchall()
    cursor.close()
    return results

def create_order(user_id, product_id, quantity, total):
    """Создание заказа с атомарными операциями"""
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                # Операция 1: Создать заказ
                cur.execute(
                    "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id",
                    (user_id, total)
                    )
                order_id = cur.fetchone()[0]

                # Операция 2: Уменьшить количество товаров
                cur.execute(
                    "UPDATE products SET quantity = quantity - %s WHERE id = %s",
                    (quantity, product_id)
                    )

                # Проверка: количество товаров не отрицательное
                cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
                result = cur.fetchone()
                if result[0] < 0:
                    raise ValueError("Недостаточно товара на складе")

                # Все операции успешны - транзакция подтверждается автоматически
                return order_id

        except Exception as e:
            # При любой ошибке все изменения откатываются автоматически
            conn.rollback()
            print(f"Ошибка при создании заказа: {e}")
            raise

def generate_sales_report(start_date):
    """Генерация отчета с правильным уровнем изоляции"""
    with get_connection() as conn:
        # Установка уровня изоляции для согласованности данных
        conn.set_isolation_level(ISOLATION_LEVEL_REPEATABLE_READ)

        try:
            with conn.cursor() as cur:
                # Первое чтение: сумма заказов
                cur.execute(
                    "SELECT COALESCE(SUM(total), 0) FROM orders WHERE created_at >= %s",
                    (start_date,)
                    )
                total = cur.fetchone()[0]

                # Второе чтение: количество заказов
                # Благодаря REPEATABLE READ данные не изменятся между чтениями
                cur.execute(
                    "SELECT COUNT(*) FROM orders WHERE created_at >= %s",
                    (start_date,)
                    )
                count = cur.fetchone()[0]

                # Данные согласованы благодаря уровню изоляции
                return {
                    "total": float(total),
                    "count": count,
                    "average": float(total) / count if count > 0 else 0
                    }

        except psycopg2.Error as e:
            conn.rollback()
            print(f"Ошибка при генерации отчета: {e}")
            raise

def create_order_with_acid(user_id, product_id, quantity, total):
    """Создание заказа с соблюдением всех ACID принципов"""
    with get_connection() as conn:
        # I - Isolation: установка уровня изоляции
        conn.set_isolation_level(ISOLATION_LEVEL_REPEATABLE_READ)

        try:
            with conn.cursor() as cur:
                # C - Consistency: проверка согласованности перед операциями
                cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
                balance = cur.fetchone()[0]
                if balance < total:
                    raise ValueError("Недостаточно средств")

                cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
                product_quantity = cur.fetchone()[0]
                if product_quantity < quantity:
                    raise ValueError("Недостаточно товара на складе")

                # A - Atomicity: все операции в одной транзакции
                cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id", (user_id, total))
                order_id = cur.fetchone()[0]

                cur.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (quantity, product_id))
                cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (total, user_id))

                # C - Consistency: проверка согласованности после операций
                cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
                new_balance = cur.fetchone()[0]
                if new_balance < 0:
                    raise ValueError("Баланс стал отрицательным")

                cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
                new_quantity = cur.fetchone()[0]
                if new_quantity < 0:
                    raise ValueError("Количество товара стало отрицательным")

                # D - Durability: COMMIT гарантирует запись на диск
                conn.commit()
                return order_id

        except Exception as e:
            # A - Atomicity: откат всех изменений при ошибке
            conn.rollback()
            print(f"Ошибка при создании заказа: {e}")
            raise

def get_all_products_from_db():
    """Все товары из PostgreSQL списком словарей - в таком виде их кладём в кэш"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, quantity FROM products")
            rows = cur.fetchall()
    return [
        {"id": row[0], "name": row[1], "price": float(row[2]), "quantity": row[3]}
        for row in rows
    ]

def get_all_products():
    """Чтение из реплики"""
    with get_connection(read_only=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products")
            return cur.fetchall()

def create_product(name, price):
    """Запись в основную БД"""
    with get_connection(read_only=False) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
