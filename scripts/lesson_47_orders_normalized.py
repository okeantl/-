import sqlite3


def build_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE users (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE products (
            id    INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            id      INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id)
        );

        CREATE TABLE order_items (
            order_id   INTEGER NOT NULL REFERENCES orders(id),
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity   INTEGER NOT NULL,
            PRIMARY KEY (order_id, product_id)
        );
        """
    )


def seed(conn: sqlite3.Connection) -> None:
    conn.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [
        (1, "Анна"),
        (2, "Борис"),
    ])
    conn.executemany("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", [
        (1, "Ноутбук", 75000.0),
        (2, "Мышь", 1500.0),
        (3, "Клавиатура", 3000.0),
    ])
    conn.executemany("INSERT INTO orders (id, user_id) VALUES (?, ?)", [
        (101, 1),
        (102, 2),
    ])
    conn.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
        [
            (101, 1, 1),
            (101, 2, 2),
            (102, 3, 1),
            (102, 2, 1),
        ],
    )


def order_totals(conn: sqlite3.Connection) -> list[tuple[str, int, float]]:
    rows = conn.execute(
        """
        SELECT u.name        AS user_name,
               o.id          AS order_id,
               SUM(p.price * oi.quantity) AS total
        FROM orders o
        JOIN users u        ON u.id = o.user_id
        JOIN order_items oi ON oi.order_id = o.id
        JOIN products p     ON p.id = oi.product_id
        GROUP BY o.id
        ORDER BY o.id
        """
    ).fetchall()
    return [(r[0], r[1], r[2]) for r in rows]


def main() -> None:
    conn = sqlite3.connect(":memory:")
    build_schema(conn)
    seed(conn)
    for user_name, order_id, total in order_totals(conn):
        print(f"Заказ {order_id} ({user_name}): {total:.2f} руб.")
    conn.close()


if __name__ == "__main__":
    main()
