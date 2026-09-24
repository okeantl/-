from abc import ABC, abstractmethod


class DeliveryStrategy(ABC):
    """Абстракция стоимости доставки (OCP)"""
    @abstractmethod
    def cost(self, order_sum: float) -> float:
        ...


class PickupDelivery(DeliveryStrategy):
    """Самовывоз — бесплатно"""
    def cost(self, order_sum: float) -> float:
        return 0.0


class CourierDelivery(DeliveryStrategy):
    """Курьер — 300 руб., но бесплатно от 5000 руб."""
    def cost(self, order_sum: float) -> float:
        return 0.0 if order_sum >= 5000 else 300.0


class PostDelivery(DeliveryStrategy):
    """Почта — фиксированные 450 руб."""
    def cost(self, order_sum: float) -> float:
        return 450.0


class Order:
    """Только хранение данных заказа (SRP)"""
    def __init__(self, order_id: int, order_sum: float):
        self.order_id = order_id
        self.order_sum = order_sum


def final_price(order: Order, delivery: DeliveryStrategy) -> float:
    """Открыт для расширения новыми стратегиями, закрыт для модификации (OCP)"""
    return order.order_sum + delivery.cost(order.order_sum)


orders = [
    (Order(1, 3000.0), CourierDelivery()),
    (Order(2, 6000.0), CourierDelivery()),
    (Order(3, 1500.0), PickupDelivery()),
    (Order(4, 2000.0), PostDelivery()),
]

for order, delivery in orders:
    strategy_name = type(delivery).__name__
    total = final_price(order, delivery)
    print(f"Заказ {order.order_id} ({strategy_name}): {total:.2f} руб.")
