import io
import unittest


class Order:
    """Заказ SFMShop: считает итог корзины и применяет скидку."""

    def __init__(self, items):
        # items: список (цена, количество)
        self.items = items

    def subtotal(self):
        return sum(price * qty for price, qty in self.items)

    def apply_discount(self, rate):
        if rate < 0 or rate > 0.5:
            raise ValueError("Ставка скидки должна быть от 0 до 0.5")
        return round(self.subtotal() * (1 - rate), 2)


class TestOrder(unittest.TestCase):
    def test_subtotal(self):
        order = Order([(1000, 2), (500, 1)])
        self.assertEqual(order.subtotal(), 2500)

    def test_apply_discount(self):
        order = Order([(2000, 1)])
        self.assertEqual(order.apply_discount(0.1), 1800.0)

    def test_zero_discount(self):
        order = Order([(1500, 2)])
        self.assertEqual(order.apply_discount(0), 3000)

    def test_invalid_discount_raises(self):
        order = Order([(1000, 1)])
        with self.assertRaises(ValueError):
            order.apply_discount(0.9)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOrder)
    # stream=io.StringIO() — служебный отчёт runner'а не попадает в наш вывод
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    print(f"Запущено тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("Все тесты прошли" if result.wasSuccessful() else "Есть упавшие тесты")
