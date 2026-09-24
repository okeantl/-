import sqlite3


def setup_db():
    """In-memory БД заказов SFMShop с тремя заказами."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, total REAL)")
    conn.executemany(
        "INSERT INTO orders (total) VALUES (?)",
        [(1500.0,), (2300.0,), (900.0,)],
    )
    conn.commit()
    return conn


def naive_report(conn, on_between_reads):
    """Наивный отчёт без изоляции: сумму и количество читаем
    двумя отдельными запросами. Между ними успевает пройти
    чужая транзакция (on_between_reads) - цифры расходятся."""
    total = conn.execute("SELECT SUM(total) FROM orders").fetchone()[0]
    on_between_reads(conn)  # параллельная вставка ровно между чтениями
    count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    return {"total": total, "count": count}


def snapshot_report(conn, on_between_reads):
    """Согласованный отчёт (имитация REPEATABLE READ):
    фиксируем один снимок данных и считаем по нему обе метрики.
    Даже если параллельная транзакция вставит заказ - отчёт
    останется согласованным."""
    snapshot = conn.execute("SELECT total FROM orders").fetchall()
    on_between_reads(conn)  # вставка происходит, но снимок уже зафиксирован
    total = sum(row[0] for row in snapshot)
    count = len(snapshot)
    return {"total": total, "count": count}


def add_order(conn):
    conn.execute("INSERT INTO orders (total) VALUES (5000.0)")
    conn.commit()


# --- Демонстрация ---
conn = setup_db()
r1 = naive_report(conn, add_order)
print(f"Наивный отчёт: сумма={r1['total']}, заказов={r1['count']}")
print(f"  расхождение: сумма по 3 заказам, а count={r1['count']} -> цифры не сходятся")

conn = setup_db()
r2 = snapshot_report(conn, add_order)
print(f"Снимок-отчёт: сумма={r2['total']}, заказов={r2['count']}")
print(f"  среднее по заказу: {round(r2['total'] / r2['count'], 2)}")
print(f"  согласован: {r2['total'] == 1500.0 + 2300.0 + 900.0 and r2['count'] == 3}")
