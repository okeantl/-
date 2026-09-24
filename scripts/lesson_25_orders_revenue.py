import sqlite3


def connect_to_db():
    """Подключение к in-memory базе данных SQLite."""
    return sqlite3.connect(":memory:")


def setup_schema(conn):
    """Создать таблицы products и orders."""
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)"
    )
    cursor.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER)"
    )
    conn.commit()
    cursor.close()


def add_product(conn, product_id, name, price):
    """Добавить товар (параметризованный INSERT)."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
        (product_id, name, price),
    )
    conn.commit()
    cursor.close()


def add_order(conn, order_id, product_id, quantity):
    """Добавить заказ (параметризованный INSERT)."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (id, product_id, quantity) VALUES (?, ?, ?)",
        (order_id, product_id, quantity),
    )
    conn.commit()
    cursor.close()


def get_order_total(conn, order_id):
    """Сумма одного заказа: цена товара * количество."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT p.price * o.quantity "
        "FROM orders o JOIN products p ON o.product_id = p.id "
        "WHERE o.id = ?",
        (order_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    return row[0]


def get_total_revenue(conn):
    """Общая выручка по всем заказам."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT p.price * o.quantity "
        "FROM orders o JOIN products p ON o.product_id = p.id"
    )
    rows = cursor.fetchall()
    cursor.close()
    return sum(row[0] for row in rows)


def main():
    conn = connect_to_db()
    try:
        setup_schema(conn)

        add_product(conn, 1, "Ноутбук", 50000.0)
        add_product(conn, 2, "Мышь", 1500.0)

        add_order(conn, 1, 1, 2)
        add_order(conn, 2, 2, 3)

        print(f"Сумма заказа 1: {get_order_total(conn, 1)}")
        print(f"Сумма заказа 2: {get_order_total(conn, 2)}")
        print(f"Общая выручка: {get_total_revenue(conn)}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
