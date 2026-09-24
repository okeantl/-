import sqlite3


def plan_operation(cur, query, params):
    """Возвращает тип доступа к таблице orders из плана запроса:
    'SEARCH' (используется индекс) или 'SCAN' (полный перебор)."""
    cur.execute("EXPLAIN QUERY PLAN " + query, params)
    for row in cur.fetchall():
        detail = row[3]
        if "orders" in detail:
            if detail.startswith("SEARCH"):
                return "SEARCH"
            if detail.startswith("SCAN"):
                return "SCAN"
    return "UNKNOWN"


def main():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            total INTEGER
        )
    """)
    # SFMShop: 1000 заказов, user_id от 1 до 50
    cur.executemany(
        "INSERT INTO orders (id, user_id, total) VALUES (?, ?, ?)",
        [(i, (i % 50) + 1, i * 10) for i in range(1, 1001)],
    )
    conn.commit()

    query = "SELECT id, total FROM orders WHERE user_id = ?"
    params = (7,)

    before = plan_operation(cur, query, params)
    print(f"До индекса: {before}")

    cur.execute("CREATE INDEX idx_orders_user_id ON orders(user_id)")

    after = plan_operation(cur, query, params)
    print(f"После индекса: {after}")

    if before == "SCAN" and after == "SEARCH":
        print("Индекс заработал: Seq Scan сменился на поиск по индексу")
    else:
        print("Индекс не повлиял на план")

    conn.close()


if __name__ == "__main__":
    main()
