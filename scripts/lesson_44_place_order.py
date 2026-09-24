import sqlite3


def setup_db():
    """Создаёт in-memory БД SFMShop с балансом пользователя и складом товара."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, quantity INTEGER CHECK (quantity >= 0))")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, total INTEGER)")
    cur.execute("INSERT INTO users (id, balance) VALUES (1, 1000)")
    cur.execute("INSERT INTO products (id, quantity) VALUES (5, 3)")
    conn.commit()
    return conn


def place_order(conn, user_id, product_id, quantity, total):
    """Атомарно создаёт заказ: списывает деньги и товар в ОДНОЙ транзакции.

    Все операции выполняются вместе или не выполняются вообще.
    При любой ошибке (в т.ч. срабатывании CHECK-ограничения) — полный откат.
    Возвращает id заказа при успехе или None при откате.
    """
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (total, user_id))
        cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
        cur.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (user_id, total))
        order_id = cur.lastrowid
        conn.commit()
        return order_id
    except sqlite3.IntegrityError:
        conn.rollback()
        return None


def snapshot(conn):
    """Возвращает текущее состояние (баланс, остаток, число заказов)."""
    cur = conn.cursor()
    balance = cur.execute("SELECT balance FROM users WHERE id = 1").fetchone()[0]
    quantity = cur.execute("SELECT quantity FROM products WHERE id = 5").fetchone()[0]
    orders = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    return balance, quantity, orders


conn = setup_db()
print("Старт:", snapshot(conn))

# Заказ 1: денег и товара хватает — транзакция проходит целиком.
order_id = place_order(conn, user_id=1, product_id=5, quantity=2, total=600)
print("Заказ 1 (id):", order_id)
print("После заказа 1:", snapshot(conn))

# Заказ 2: денег хватает (400 > 300), а товара на складе нет (осталось 1, просят 3).
# Списание денег УЖЕ выполнилось, но CHECK на quantity срабатывает —
# атомарность откатывает всю транзакцию: баланс и склад не меняются.
order_id = place_order(conn, user_id=1, product_id=5, quantity=3, total=300)
print("Заказ 2 (id):", order_id)
print("После заказа 2:", snapshot(conn))
