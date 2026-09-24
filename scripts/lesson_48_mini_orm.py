import sqlite3
from decimal import Decimal


class User:
    """Модель пользователя — мини-ORM поверх sqlite3"""

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], name=row[1], email=row[2])


class Order:
    """Модель заказа"""

    def __init__(self, id, user_id, total):
        self.id = id
        self.user_id = user_id
        self.total = Decimal(str(total))

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], user_id=row[1], total=row[2])


def setup(conn):
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL)")
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [(1, "Иван", "ivan@test.ru"), (2, "Мария", "maria@test.ru")],
    )
    conn.executemany(
        "INSERT INTO orders (id, user_id, total) VALUES (?, ?, ?)",
        [(1, 1, 1500.0), (2, 1, 2300.0), (3, 2, 990.0)],
    )
    conn.commit()


def get_user_with_orders(conn, user_id):
    """Один запрос с JOIN: пользователь и его заказы (решение N+1)"""
    cur = conn.execute(
        """
        SELECT u.id, u.name, u.email, o.id, o.user_id, o.total
        FROM users u
        JOIN orders o ON o.user_id = u.id
        WHERE u.id = ?
        ORDER BY o.id
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    if not rows:
        return None
    user = User.from_row(rows[0][:3])
    orders = [Order.from_row(r[3:]) for r in rows]
    total_sum = sum((o.total for o in orders), Decimal("0"))
    return {
        "name": user.name,
        "email": user.email,
        "orders": [o.id for o in orders],
        "total_sum": total_sum,
    }


def main():
    conn = sqlite3.connect(":memory:")
    setup(conn)
    info = get_user_with_orders(conn, 1)
    print(f"Пользователь: {info['name']} <{info['email']}>")
    print(f"Заказы: {info['orders']}")
    print(f"Сумма заказов: {info['total_sum']}")
    conn.close()


if __name__ == "__main__":
    main()
