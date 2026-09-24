from src.models.product import DiscountStrategy, Product


class ProductCalculator:
    """Класс для расчетов товара (SRP)"""

    @staticmethod
    def calculate_total_value(product: Product) -> float:
        """Рассчитать общую стоимость партии товара"""
        return product.get_total_price()

    @staticmethod
    def apply_discount(product: Product, discount: DiscountStrategy) -> float:
        """Применить скидку к цене товара"""
        return discount.apply(product.price)
