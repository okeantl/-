import sys
from pathlib import Path

# Корень проекта в sys.path, чтобы импорт src.* работал при запуске файла напрямую
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.models.product import Product


if __name__ == "__main__":
    raw_products = [
        {"name": "Ноутбук", "price": 1000, "quantity": 10},
        {"name": "Мышь", "price": 500, "quantity": 20},
        {"name": "Клавиатура", "price": 800, "quantity": 5},
    ]

    products = [Product.from_dict(item) for item in raw_products]

    for product in products:
        sale_price = Product.calculate_discount(product.price, 25)
        print(f"{product.name}: {product.price} -> {sale_price}")
