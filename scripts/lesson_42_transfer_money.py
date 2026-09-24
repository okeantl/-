import sqlite3


def setup_db():
    """Создаёт in-memory БД SFMShop с балансами пользователей."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
    conn.executemany(
        "INSERT INTO users (id, name, balance) VALUES (?, ?, ?)",
        [(1, "Анна", 5000), (2, "Борис", 1000), (3, "Вера", 200)],
    )
    conn.commit()
    return conn


def transfer_money(conn, from_id, to_id, amount):
    """Перевод денег между пользователями SFMShop в одной транзакции.

    Возвращает True при успехе, False при откате (недостаточно средств).
    """
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, from_id))
        cur.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, to_id))

        cur.execute("SELECT balance FROM users WHERE id = ?", (from_id,))
        if cur.fetchone()[0] < 0:
            raise ValueError("Недостаточно средств")

        conn.commit()
        return True
    except ValueError:
        conn.rollback()
        return False


def balance(conn, user_id):
    return conn.execute("SELECT balance FROM users WHERE id = ?", (user_id,)).fetchone()[0]


conn = setup_db()

# Успешный перевод: Анна -> Борис 1500
ok = transfer_money(conn, 1, 2, 1500)
print(f"Перевод 1: {'успех' if ok else 'откат'}, баланс Анны={balance(conn, 1)}, баланс Бориса={balance(conn, 2)}")

# Откат: Вера пытается перевести 500, но у неё только 200
ok = transfer_money(conn, 3, 2, 500)
print(f"Перевод 2: {'успех' if ok else 'откат'}, баланс Веры={balance(conn, 3)}, баланс Бориса={balance(conn, 2)}")
