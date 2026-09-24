import sqlite3


def setup_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER)")
    cur.execute("CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER)")
    cur.executemany("INSERT INTO products VALUES (?, ?, ?)", [
        (1, "Клавиатура", 5000),
        (2, "Мышь", 2000),
        (3, "Монитор", 25000),
        (4, "Коврик", 800),
    ])
    cur.executemany("INSERT INTO orders VALUES (?, ?)", [
        (1, 10), (2, 10), (3, 20),
    ])
    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", [
        (1, 1, 1, 2),   # заказ 1: 2 клавиатуры
        (2, 1, 2, 3),   # заказ 1: 3 мыши
        (3, 2, 3, 1),   # заказ 2: 1 монитор
        (4, 2, 2, 2),   # заказ 2: 2 мыши
        (5, 3, 1, 1),   # заказ 3: 1 клавиатура
        (6, 3, 4, 5),   # заказ 3: 5 ковриков
    ])
    conn.commit()
    return conn


def top_products_by_revenue(conn, limit):
    """Топ товаров по выручке: имя и суммарная выручка (quantity * price)."""
    cur = conn.cursor()
    cur.execute("""
        SELECT products.name,
               SUM(order_items.quantity * products.price) AS revenue
        FROM order_items
        INNER JOIN products ON order_items.product_id = products.id
        GROUP BY products.id
        ORDER BY revenue DESC, products.name ASC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    return rows


if __name__ == "__main__":
    conn = setup_db()
    for name, revenue in top_products_by_revenue(conn, 3):
        print(f"{name}: {revenue}")
    conn.close()
