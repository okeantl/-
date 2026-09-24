from abc import ABC, abstractmethod


class ShippingStrategy(ABC):
    @abstractmethod
    def cost(self, weight: float) -> float:
        pass


class CourierShipping(ShippingStrategy):
    def cost(self, weight: float) -> float:
        return 300 + 50 * weight


class PickupShipping(ShippingStrategy):
    def cost(self, weight: float) -> float:
        return 0.0


class PostShipping(ShippingStrategy):
    def cost(self, weight: float) -> float:
        return 200 + 20 * weight


class ShippingCalculator:
    @staticmethod
    def calculate(weight: float, strategy: ShippingStrategy) -> float:
        return strategy.cost(weight)


orders = [
    ("Заказ №1", 4.0, CourierShipping()),
    ("Заказ №2", 4.0, PickupShipping()),
    ("Заказ №3", 4.0, PostShipping()),
]

for name, weight, strategy in orders:
    cost = ShippingCalculator.calculate(weight, strategy)
    print(f"{name}: {cost:.2f} руб.")
