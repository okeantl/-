import sqlite3


def setup_database():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn


def seed(conn):
    users = [
        (1, "Анна", "anna@sfmshop.ru"),
        (2, "Борис", "boris@sfmshop.ru"),
    ]
    products = [
        (1, "Клавиатура", 2500.0),
        (2, "Мышь", 900.0),
        (3, "Монитор", 15000.0),
    ]
    orders = [
        (1, 1, 1, 2),
        (2, 1, 3, 1),
        (3, 2, 2, 3),
    ]
    conn.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
    conn.executemany("INSERT INTO products VALUES (?, ?, ?)", products)
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    conn.commit()


def report(conn):
    cur = conn.execute("""
        SELECT u.name, SUM(p.price * o.quantity) AS total
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
        GROUP BY u.id
        ORDER BY total DESC
    """)
    for name, total in cur.fetchall():
        print(f"{name}: {total:.2f}")


if __name__ == "__main__":
    conn = setup_database()
    seed(conn)
    report(conn)
    conn.close()
