from abc import ABC, abstractmethod

class Delivery(ABC):
    """Абстрактный класс для доставки"""

    @abstractmethod
    def calculate_cost(self, distance: float) -> float:
        """Рассчитать стоимость доставки"""
        pass

class StandardDelivery(Delivery):
    """Стандартная доставка"""

    def calculate_cost(self, distance: float) -> float:
        """Стоимость = расстояние * 10"""
        return distance * 10

class ExpressDelivery(Delivery):
    """Экспресс-доставка"""

    def calculate_cost(self, distance: float) -> float:
        """Стоимость = расстояние * 20"""
        return distance * 20

# Пример использования (полиморфизм)
def process_delivery(delivery: Delivery, distance: float) -> float:
    """Обработать доставку - работает с любым типом Delivery"""
    return delivery.calculate_cost(distance)

# Использование
if __name__ == "__main__":
    standard = StandardDelivery()
    express = ExpressDelivery()

    cost1 = process_delivery(standard, 5.0)  # 50.0
    cost2 = process_delivery(express, 5.0)  # 100.0

    print(f"Стандартная доставка: {cost1} руб.")
    print(f"Экспресс-доставка: {cost2} руб.")
