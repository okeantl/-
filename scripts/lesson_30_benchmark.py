import sys
from pathlib import Path

# Корень проекта в sys.path, чтобы импорт src.* работал при запуске файла напрямую
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.models.order import Order
from src.models.product import Product
from src.models.user import User
from src.utils.calculations import benchmark_calculate_total


def build_orders(copies=1000):
    """Собрать список заказов для замера: три заказа, повторённые copies раз"""
    user = User("Иван Петров", "ivan@example.com")
    orders = [
        Order(user, [Product("Ноутбук", 50000, 2), Product("Мышь", 1500, 1)]),
        Order(user, [Product("Клавиатура", 3000, 3), Product("Коврик", 500, 5)]),
        Order(user, [Product("Монитор", 20000, 1)]),
    ]
    return orders * copies


# Пример использования
if __name__ == "__main__":
    benchmark_calculate_total(build_orders())
