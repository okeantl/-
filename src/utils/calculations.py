import time


def calculate_discount(price, discount_rate):
    return price * discount_rate


def calculate_total(price, quantity):
    return price * quantity


def calculate_delivery(weight: float, distance: float) -> float:
    """Рассчитать стоимость доставки

    Args:
        weight: Вес товара в кг
        distance: Расстояние в км

    Returns:
        Стоимость доставки в рублях
    """
    # Реализовано через TDD: Красный -> Зелёный -> Рефакторинг
    base_price = 100  # Базовая стоимость
    weight_price = weight * 10  # 10 руб за кг
    distance_price = distance * 5  # 5 руб за км

    return base_price + weight_price + distance_price

# Исходная функция (медленная) — O(N * M)
# на каждый вызов заново обходит товары всех заказов


def calculate_total_orders_slow(orders):
    """Медленный подход: каждый раз обходит товары каждого заказа"""
    total = 0
    for order in orders:
        for product in order.products:
            total += product.get_total_price()
    return total

# Оптимизированная функция (быстрая) — O(N)
# суммы заказов посчитаны заранее, здесь их только складывают


def calculate_total_orders(order_totals):
    """Быстрый подход: сумма по заранее посчитанным суммам заказов"""
    return sum(order_totals)

# Измерение производительности


def benchmark_calculate_total(orders):
    """Измерить производительность обеих функций"""
    # Медленная версия
    start_time = time.time()
    result_slow = calculate_total_orders_slow(orders)
    time_slow = time.time() - start_time

    # Суммы заказов считаем один раз — в реальном коде это делают
    # при создании заказа, а не на каждый отчёт
    order_totals = [order.calculate_total() for order in orders]

    # Быстрая версия
    start_time = time.time()
    result_fast = calculate_total_orders(order_totals)
    time_fast = time.time() - start_time

    # Сравнение
    speedup = time_slow / time_fast if time_fast > 0 else 0

    print(f"Медленная версия: {time_slow:.4f} секунд")
    print(f"Быстрая версия: {time_fast:.4f} секунд")
    print(f"Ускорение: {speedup:.2f}x")
    print(f"Результаты совпадают: {result_slow == result_fast}")

    return {
        "time_slow": time_slow,
        "time_fast": time_fast,
        "speedup": speedup,
        "result": result_fast,
    }
