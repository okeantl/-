from abc import ABC, abstractmethod


class Discount(ABC):
    """Абстрактный класс скидки"""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Вернуть итоговую сумму после применения скидки"""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Короткое описание скидки"""
        pass


class PercentDiscount(Discount):
    """Процентная скидка"""

    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)

    def describe(self) -> str:
        return f"-{self.percent:.0f}%"


class FixedDiscount(Discount):
    """Фиксированная скидка в рублях"""

    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount)

    def describe(self) -> str:
        return f"-{self.amount:.0f} руб."


class Cart:
    """Корзина SFMShop: ИМЕЕТ скидку (композиция)"""

    def __init__(self, discount: Discount):
        self.discount = discount
        self.items = []

    def add(self, name: str, price: float) -> None:
        self.items.append((name, price))

    def total(self) -> float:
        base = sum(price for _, price in self.items)
        return self.discount.apply(base)


def checkout(cart: Cart) -> None:
    """Полиморфизм: работает с любой скидкой"""
    print(f"Товаров в корзине: {len(cart.items)}")
    print(f"Скидка: {cart.discount.describe()}")
    print(f"К оплате: {cart.total():.2f} руб.")


# Использование
cart1 = Cart(PercentDiscount(20))
cart1.add("Футболка", 1500)
cart1.add("Кепка", 1000)
checkout(cart1)

cart2 = Cart(FixedDiscount(500))
cart2.add("Худи", 3000)
checkout(cart2)
