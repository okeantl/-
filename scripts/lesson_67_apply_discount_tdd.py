import unittest


def apply_discount(price: float, quantity: int) -> float:
    """Итоговая стоимость с учётом скидки за количество в SFMShop.

    Скидка:
      - меньше 3 шт      -> 0%
      - от 3 до 5 шт     -> 5%
      - 6 шт и больше    -> 10%
    """
    subtotal = price * quantity
    if quantity >= 6:
        rate = 0.10
    elif quantity >= 3:
        rate = 0.05
    else:
        rate = 0.0
    return subtotal * (1 - rate)


class TestApplyDiscount(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(apply_discount(100, 2), 200.0)

    def test_five_percent(self):
        self.assertEqual(apply_discount(100, 4), 380.0)

    def test_ten_percent(self):
        self.assertEqual(apply_discount(100, 10), 900.0)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestApplyDiscount)
    result = unittest.TestResult()
    suite.run(result)
    print(f"Запущено тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("Все тесты прошли" if result.wasSuccessful() else "Есть падения")
    print(f"apply_discount(100, 2) = {apply_discount(100, 2)}")
    print(f"apply_discount(100, 4) = {apply_discount(100, 4)}")
    print(f"apply_discount(100, 10) = {apply_discount(100, 10)}")
