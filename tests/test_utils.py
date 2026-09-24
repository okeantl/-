import pytest
from src.utils.calculations import calculate_discount, calculate_delivery


def test_calculate_discount_no_discount():
    """Тест: нулевая ставка - нет скидки"""
    assert calculate_discount(500, 0) == 0


def test_calculate_discount_5_percent():
    """Тест: ставка 5%"""
    assert calculate_discount(2000, 0.05) == 100  # 5% от 2000
    assert calculate_discount(2500, 0.05) == 125  # 5% от 2500


def test_calculate_discount_10_percent():
    """Тест: ставка 10%"""
    assert calculate_discount(6000, 0.1) == 600  # 10% от 6000
    assert calculate_discount(7500, 0.1) == 750  # 10% от 7500


def test_calculate_discount_15_percent():
    """Тест: ставка 15%"""
    assert calculate_discount(15000, 0.15) == 2250  # 15% от 15000
    assert calculate_discount(20000, 0.15) == 3000  # 15% от 20000


# Параметризация для всех случаев
@pytest.mark.parametrize("price,rate,expected", [
    (500, 0, 0),
    (2000, 0.05, 100),
    (2500, 0.05, 125),
    (6000, 0.1, 600),
    (7500, 0.1, 750),
    (15000, 0.15, 2250),
    (20000, 0.15, 3000),
])
def test_calculate_discount_all_cases(price, rate, expected):
    """Тест: все случаи расчета скидки"""
    assert calculate_discount(price, rate) == expected


# --- TDD: расчёт стоимости доставки (Красный -> Зелёный -> Рефакторинг) ---


def test_calculate_delivery():
    """Тест: расчет стоимости доставки"""
    result = calculate_delivery(weight=5, distance=50)
    assert result == 400


@pytest.mark.parametrize("weight,distance,expected", [
    (1, 10, 160),   # 100 + 1*10 + 10*5 = 160
    (5, 50, 400),   # 100 + 5*10 + 50*5 = 400
    (10, 100, 700),  # 100 + 10*10 + 100*5 = 700
])
def test_calculate_delivery_cases(weight, distance, expected):
    """Тест: расчет доставки для разных случаев"""
    assert calculate_delivery(weight, distance) == expected
