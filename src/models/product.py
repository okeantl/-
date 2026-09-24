from abc import ABC, abstractmethod

from src.models.descriptors import PositiveNumber
from src.models.metaclasses import ModelMeta
from src.models.mixins import LoggableMixin, SerializableMixin


class DiscountStrategy(ABC):
    """Абстрактный класс для стратегий скидок (OCP)"""

    @abstractmethod
    def apply(self, price: float) -> float:
        """Применить скидку к цене"""
        pass


class PercentDiscount(DiscountStrategy):
    """Скидка в процентах"""

    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    """Фиксированная скидка"""

    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, price: float) -> float:
        return max(0, price - self.amount)


class Product(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    """Данные товара и цена со скидкой через стратегию (OCP)"""

    price = PositiveNumber("_price")
    quantity = PositiveNumber("_quantity")

    def __init__(self, name, price, quantity=0):
        self.name = name
        self.price = price  # валидация — в дескрипторе
        self.quantity = quantity  # валидация — в дескрипторе
        self.log(f"Создан товар: {name}, цена: {price}")

    def get_total_price(self):
        """Общая стоимость партии товара (из урока 15)"""
        return self.price * self.quantity

    @classmethod
    def from_dict(cls, data):
        """Альтернативный конструктор из словаря (урок 34)"""
        return cls(data["name"], data["price"], data["quantity"])

    @staticmethod
    def calculate_discount(price, discount_percent):
        """Цена со скидкой в процентах (урок 34)"""
        return price * (1 - discount_percent / 100)

    def calculate_price(self, discount: DiscountStrategy = None) -> float:
        """Расчет цены со скидкой - открыт для расширения (OCP)"""
        if discount is None:
            return self.price
        return discount.apply(self.price)

    def to_json(self):
        # Переопределяет SerializableMixin.to_json (строка JSON из __dict__):
        # модели нужен словарь с публичными именами полей — его сериализует API
        return {"name": self.name, "price": self.price, "quantity": self.quantity}

    def __str__(self):
        return f"{self.name}: {self.price} руб. (в наличии: {self.quantity})"

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (self.name, self.price, self.quantity) == (
            other.name,
            other.price,
            other.quantity,
        )

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price
