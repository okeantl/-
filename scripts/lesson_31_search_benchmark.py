import time

class Product:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def linear_search(products, product_id):
    """Линейный поиск в списке (O(n))"""
    for product in products:
        if product.id == product_id:
            return product
    return None

def dict_search(products_dict, product_id):
    """Поиск в словаре (O(1))"""
    return products_dict.get(product_id)

def compare_search_methods():
    """Сравнить время поиска в списке vs словаре"""
    # Создать большой список товаров
    products = [Product(i, f"Товар {i}") for i in range(10000)]

    # Создать словарь
    products_dict = {product.id: product for product in products}

    # Товар для поиска (в середине списка)
    product_id = 5000

    # Измерить время поиска в списке
    start_time = time.time()
    result_list = linear_search(products, product_id)
    time_list = time.time() - start_time

    # Измерить время поиска в словаре
    start_time = time.time()
    result_dict = dict_search(products_dict, product_id)
    time_dict = time.time() - start_time

    # Сравнение
    speedup = time_list / time_dict if time_dict > 0 else 0

    print(f"Поиск в списке: {time_list:.6f} секунд")
    print(f"Поиск в словаре: {time_dict:.6f} секунд")
    print(f"Ускорение: {speedup:.2f}x")
    print(f"Результаты совпадают: {result_list == result_dict}")
    print(f"\nОбъяснение:")
    print(f"- Линейный поиск имеет сложность O(n) - нужно проверить все элементы")
    print(f"- Поиск в словаре имеет сложность O(1) - константное время")
    print(f"- Для больших данных разница становится критической")

    return {
        "time_list": time_list,
        "time_dict": time_dict,
        "speedup": speedup
        }

if __name__ == "__main__":
    compare_search_methods()
