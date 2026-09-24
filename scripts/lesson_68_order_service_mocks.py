from unittest.mock import MagicMock


# --- Код SFMShop, который мы тестируем (дан) ---
class OrderService:
    """Оформляет заказ: пишет в БД и шлёт уведомление."""

    def __init__(self, db, notifier):
        self.db = db
        self.notifier = notifier

    def place_order(self, user_id, items):
        # items: список (product_id, qty, price)
        if not items:
            raise ValueError("Пустой заказ")
        total = sum(qty * price for _, qty, price in items)
        order_id = self.db.create_order(user_id=user_id, total=total)
        self.notifier.send(user_id=user_id, text=f"Заказ #{order_id} на {total} руб.")
        return order_id


# --- Решение: тестируем с моками, без реальной БД и почты ---
def test_place_order_happy_path():
    mock_db = MagicMock()
    mock_db.create_order.return_value = 42
    mock_notifier = MagicMock()

    service = OrderService(mock_db, mock_notifier)
    items = [(1, 2, 1500), (3, 1, 2000)]  # 2*1500 + 1*2000 = 5000
    order_id = service.place_order(user_id=7, items=items)

    assert order_id == 42
    mock_db.create_order.assert_called_once_with(user_id=7, total=5000)
    mock_notifier.send.assert_called_once_with(
        user_id=7, text="Заказ #42 на 5000 руб."
    )
    print("happy_path: ok, order_id =", order_id)


def test_place_order_empty_raises():
    mock_db = MagicMock()
    mock_notifier = MagicMock()
    service = OrderService(mock_db, mock_notifier)

    raised = False
    try:
        service.place_order(user_id=7, items=[])
    except ValueError:
        raised = True

    assert raised is True
    mock_db.create_order.assert_not_called()
    mock_notifier.send.assert_not_called()
    print("empty_raises: ok, БД и уведомление не дёрнуты")


def test_db_failure_no_notification():
    mock_db = MagicMock()
    mock_db.create_order.side_effect = RuntimeError("DB down")
    mock_notifier = MagicMock()
    service = OrderService(mock_db, mock_notifier)

    raised = False
    try:
        service.place_order(user_id=7, items=[(1, 1, 999)])
    except RuntimeError:
        raised = True

    assert raised is True
    mock_notifier.send.assert_not_called()
    print("db_failure: ok, уведомление не ушло при падении БД")


def main():
    for test in (
        test_place_order_happy_path,
        test_place_order_empty_raises,
        test_db_failure_no_notification,
    ):
        test()
    print("Все тесты прошли")


if __name__ == "__main__":
    main()
