"""Тесты для src/utils/calculations.py."""

import pytest

from src.utils.calculations import (
    benchmark_calculate_total,
    calculate_delivery,
    calculate_discount,
    calculate_total,
    calculate_total_orders,
    calculate_total_orders_slow,
)


# ==================== calculate_discount ====================
# Функция возвращает не итоговую цену, а размер скидки: price * discount_rate


class TestCalculateDiscount:
    def test_zero_rate(self):
        assert calculate_discount(500, 0) == 0

    def test_zero_price(self):
        assert calculate_discount(0, 0.05) == 0

    @pytest.mark.parametrize(
        "price,rate,expected",
        [
            (2000, 0.05, 100),
            (2500, 0.05, 125),
            (6000, 0.10, 600),
            (7500, 0.10, 750),
            (15000, 0.15, 2250),
            (20000, 0.15, 3000),
            (1000, 0.0, 0),
            (1000, 1.0, 1000),
        ],
    )
    def test_typical_rates(self, price, rate, expected):
        assert calculate_discount(price, rate) == expected

    def test_rate_as_percent_not_fraction(self):
        # Если передать 10 вместо 0.1 — получим 1000*10 = 10000.
        # Тест фиксирует текущее поведение (функция не валидирует rate).
        assert calculate_discount(1000, 10) == 10000

    def test_negative_rate_decreases_discount(self):
        # Отрицательная ставка → скидка отрицательная (надбавка)
        assert calculate_discount(1000, -0.1) == -100

    def test_large_values(self):
        assert calculate_discount(10_000_000, 0.05) == 500_000


# ==================== calculate_delivery ====================
# Формула: base 100 + weight * 10 + distance * 5


class TestCalculateDelivery:
    def test_zero_weight_zero_distance(self):
        # 100 + 0 + 0
        assert calculate_delivery(0, 0) == 100

    def test_only_weight(self):
        # 100 + 5*10 + 0 = 150
        assert calculate_delivery(5, 0) == 150

    def test_only_distance(self):
        # 100 + 0 + 50*5 = 350
        assert calculate_delivery(0, 50) == 350

    @pytest.mark.parametrize(
        "weight,distance,expected",
        [
            (1, 10, 160),  # 100 + 10 + 50
            (5, 50, 400),  # 100 + 50 + 250
            (10, 100, 700),  # 100 + 100 + 500
            (0, 0, 100),  # базовая стоимость
            (2, 0, 120),  # 100 + 20
            (0, 20, 200),  # 100 + 100
        ],
    )
    def test_typical_cases(self, weight, distance, expected):
        assert calculate_delivery(weight, distance) == expected

    def test_float_values(self):
        # 100 + 1.5*10 + 10.5*5 = 100 + 15 + 52.5 = 167.5
        assert calculate_delivery(1.5, 10.5) == 167.5

    def test_negative_weight_gives_less_than_base(self):
        # Функция не валидирует — фиксируем поведение
        assert calculate_delivery(-5, 0) == 50

    def test_large_values(self):
        # 100 + 1000*10 + 10000*5 = 100 + 10000 + 50000 = 60100
        assert calculate_delivery(1000, 10000) == 60100


# ==================== calculate_total ====================
# Формула: price * quantity


class TestCalculateTotal:
    @pytest.mark.parametrize(
        "price,quantity,expected",
        [
            (1000, 3, 3000),
            (1500, 0, 0),
            (0, 5, 0),
            (999.99, 2, 1999.98),
            (50000, 10, 500000),
        ],
    )
    def test_cases(self, price, quantity, expected):
        assert calculate_total(price, quantity) == expected

    def test_negative_quantity(self):
        # Не валидируется — фиксируем поведение
        assert calculate_total(100, -1) == -100


# ==================== calculate_total_orders ====================


class TestCalculateTotalOrders:
    def test_empty_list(self):
        assert calculate_total_orders([]) == 0

    def test_single_order(self):
        assert calculate_total_orders([1500]) == 1500

    def test_multiple_orders(self):
        assert calculate_total_orders([1500, 2000, 500]) == 4000

    def test_with_floats(self):
        result = calculate_total_orders([100.5, 200.25])
        assert result == pytest.approx(300.75)


class TestCalculateTotalOrdersSlow:
    def test_empty_list(self):
        assert calculate_total_orders_slow([]) == 0

    def test_single_order(self, sample_order):
        # sample_order: 1 товар Product("Ноутбук", 50000, 10)
        # get_total_price() = 500000
        assert calculate_total_orders_slow([sample_order]) == 500000

    def test_matches_fast_version(self, sample_user, sample_products):
        """Медленная и быстрая версии должны давать одинаковый результат."""
        from src.models.order import Order

        orders = [
            Order(user=sample_user, products=sample_products),
            Order(user=sample_user, products=sample_products),
        ]
        slow = calculate_total_orders_slow(orders)
        totals = [o.calculate_total() for o in orders]
        fast = calculate_total_orders(totals)
        assert slow == fast
        # 56000 * 2 = 112000
        assert slow == 112000


# ==================== benchmark ====================


class TestBenchmark:
    def test_returns_expected_keys(self, sample_order):
        result = benchmark_calculate_total([sample_order])
        assert set(result.keys()) == {"time_slow", "time_fast", "speedup", "result"}

    def test_result_is_number(self, sample_order):
        result = benchmark_calculate_total([sample_order])
        assert result["result"] == sample_order.calculate_total()

    def test_times_are_non_negative(self, sample_order):
        result = benchmark_calculate_total([sample_order])
        assert result["time_slow"] >= 0
        assert result["time_fast"] >= 0
        assert result["speedup"] >= 0
