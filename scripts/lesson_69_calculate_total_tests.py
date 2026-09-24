import unittest


def calculate_total(price, quantity, discount_rate):
    """Считает итоговую стоимость позиции заказа SFMShop с учётом скидки.

    price - цена за единицу, quantity - количество, discount_rate - доля скидки (0..1).
    """
    if price < 0 or quantity < 0:
        raise ValueError("price и quantity не могут быть отрицательными")
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate должен быть в диапазоне от 0 до 1")
    subtotal = price * quantity
    return round(subtotal * (1 - discount_rate), 2)


class TestCalculateTotal(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(calculate_total(100, 3, 0), 300)

    def test_with_discount(self):
        self.assertEqual(calculate_total(1000, 1, 0.2), 800.0)

    def test_zero_quantity(self):
        self.assertEqual(calculate_total(500, 0, 0.1), 0.0)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            calculate_total(-50, 2, 0.0)

    def test_invalid_discount_raises(self):
        with self.assertRaises(ValueError):
            calculate_total(100, 1, 1.5)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculateTotal)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    print(f"Запущено тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("Все тесты прошли" if result.wasSuccessful() else "Есть упавшие тесты")


if __name__ == "__main__":
    main()
