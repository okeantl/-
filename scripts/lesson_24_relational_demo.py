import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")
cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        total REAL NOT NULL
    )
""")

users = [(1, "Иван"), (2, "Мария")]
cur.executemany("INSERT INTO users (id, name) VALUES (?, ?)", users)

orders = [(1, 1, 1500.0), (2, 1, 500.0), (3, 2, 3000.0)]
cur.executemany("INSERT INTO orders (id, user_id, total) VALUES (?, ?, ?)", orders)

# Пытаемся создать заказ для несуществующего пользователя (id=99)
try:
    cur.execute("INSERT INTO orders (id, user_id, total) VALUES (?, ?, ?)", (4, 99, 100.0))
    conn.commit()
    print("Заказ для пользователя 99 создан")
except sqlite3.IntegrityError:
    print("Заказ для несуществующего пользователя отклонён")

# Сумма заказов по каждому пользователю через JOIN
cur.execute("""
    SELECT users.name, SUM(orders.total) AS total_sum
    FROM users
    JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    ORDER BY total_sum DESC
""")
for name, total_sum in cur.fetchall():
    print(f"{name}: {total_sum:.0f}")

conn.close()
