import unittest


def order_total(items, discount_percent=0):
    """items: список (цена, количество). Возвращает сумму со скидкой,
    округлённую до 2 знаков. discount_percent в диапазоне 0..100."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    subtotal = sum(price * qty for price, qty in items)
    total = subtotal * (1 - discount_percent / 100)
    return round(total, 2)


class TestOrderTotal(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(order_total([(100.0, 2), (50.0, 1)]), 250.0)

    def test_with_discount(self):
        self.assertEqual(order_total([(100.0, 2), (50.0, 1)], 10), 225.0)

    def test_empty_order(self):
        self.assertEqual(order_total([]), 0.0)

    def test_invalid_discount(self):
        with self.assertRaises(ValueError):
            order_total([(100.0, 1)], 150)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOrderTotal)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    print(f"Запущено тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("CI статус: PASS" if result.wasSuccessful() else "CI статус: FAIL")
