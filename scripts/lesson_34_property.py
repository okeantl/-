class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price  # пройдёт через сеттер

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value


product = Product("Ноутбук", 1000)
print(product.price)  # 1000

try:
    product.price = -100  # перехватывается сеттером
except ValueError as e:
    print(f"Ошибка при изменении: {e}")

product.price = 2000  # корректное изменение — проходит валидацию
print(product.price)  # 2000
