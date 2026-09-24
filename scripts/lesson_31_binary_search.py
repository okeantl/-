
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


def binary_search_by_id(sorted_products, target_id):
    """Бинарный поиск товара по ID в отсортированном по ID списке (O(log n))."""
    left = 0
    right = len(sorted_products) - 1
    while left <= right:
        mid = (left + right) // 2
        current_id = sorted_products[mid].id
        if current_id == target_id:
            return sorted_products[mid]
        elif current_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return None


def main():
    products = [
        Product(105, "Мышь", 1500),
        Product(101, "Ноутбук", 50000),
        Product(110, "Монитор", 18000),
        Product(103, "Клавиатура", 3000),
        Product(108, "Наушники", 7000),
    ]

    # Бинарный поиск работает только на отсортированном списке
    sorted_products = sorted(products, key=lambda p: p.id)

    print("Каталог, отсортированный по ID:")
    for product in sorted_products:
        print(f"  ID {product.id}: {product.name} - {product.price} руб.")

    for target_id in [108, 110, 104]:
        found = binary_search_by_id(sorted_products, target_id)
        if found is not None:
            print(f"Поиск ID {target_id}: найден товар '{found.name}'")
        else:
            print(f"Поиск ID {target_id}: товар не найден")


if __name__ == "__main__":
    main()
