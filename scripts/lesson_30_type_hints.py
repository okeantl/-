from typing import Optional


def calculate_discount(price: float, percent: float) -> float:
    return price * (1 - percent / 100)


def find_product(products: list[dict], product_id: int) -> Optional[dict]:
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def get_product_names(products: list[dict]) -> list[str]:
    names = []
    for product in products:
        names.append(product["name"])
    return names

# Проверка
products = [
    {"id": 1, "name": "Ноутбук", "price": 50000},
    {"id": 2, "name": "Мышь", "price": 1500}
    ]

print(calculate_discount(1000.0, 10.0)) # 900.0
print(find_product(products, 1)) # {'id': 1, 'name': 'Ноутбук', 'price': 50000}
print(find_product(products, 99)) # None
print(get_product_names(products)) # ['Ноутбук', 'Мышь']
