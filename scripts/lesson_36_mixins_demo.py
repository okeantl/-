import sys
from pathlib import Path

# Корень проекта в sys.path, чтобы импорт src.* работал при запуске файла напрямую
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.models.product import Product


class DiscountableMixin:
    """Миксин для расчёта цены со скидкой"""

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Процент скидки должен быть от 0 до 100")
        discounted = self.price * (1 - percent / 100)
        return round(discounted, 2)


class DictSerializableMixin:
    """Миксин для представления объекта в виде словаря
    (не путать с SerializableMixin.to_json из урока — тот отдаёт JSON-строку)"""

    def to_dict(self):
        return {"class": self.__class__.__name__, "data": self.__dict__}


class DiscountableProduct(DiscountableMixin, DictSerializableMixin, Product):
    """Тот же Product из src/models/product.py плюс два умения из этого файла"""


if __name__ == "__main__":
    product = DiscountableProduct("Ноутбук", 1000, 5)

    print(product.apply_discount(15))
    print(product.apply_discount(0))
    print(product.to_dict())

    try:
        product.apply_discount(150)
    except ValueError as e:
        print(f"Ошибка: {e}")

    print([cls.__name__ for cls in DiscountableProduct.__mro__])
