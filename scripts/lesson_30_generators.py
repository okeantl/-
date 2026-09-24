def expensive_products(products, min_price):
    """Генератор: отдаёт товары дороже min_price по одному"""
    for product in products:
        if product["price"] > min_price:
            yield product

products = [
    {"name": "Ноутбук", "price": 50000},
    {"name": "Мышь", "price": 1500},
    {"name": "Монитор", "price": 25000},
    {"name": "Клавиатура", "price": 3000},
    {"name": "Наушники", "price": 8000}
    ]

# Используем генератор в цикле
print("Дорогие товары (дороже 5000):")
for product in expensive_products(products, 5000):
    print(f"- {product['name']}: {product['price']} руб.")

# Используем генератор для подсчёта суммы
total = sum(p["price"] for p in expensive_products(products, 5000))
print(f"Сумма дорогих товаров: {total} руб.")
