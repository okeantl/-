"""Тесты для моделей src/models/ (Product, User, Order и вспомогательные)."""

import pytest

from src.models.descriptors import PositiveNumber
from src.models.exceptions import (
    InsufficientStockError,
    InvalidOrderError,
    NegativePriceError,
    SFMShopException,
)
from src.models.order import Order, OrderCalculator, OrderValidator
from src.models.product import (
    DiscountStrategy,
    FixedDiscount,
    PercentDiscount,
    Product,
)
from src.models.user import User

# ==================== Product ====================


class TestProduct:
    def test_create_product(self):
        p = Product("Ноутбук", 50000, 10)
        assert p.name == "Ноутбук"
        assert p.price == 50000
        assert p.quantity == 10

    def test_get_total_price(self):
        p = Product("Ноутбук", 50000, 3)
        assert p.get_total_price() == 150000

    def test_zero_quantity_is_allowed(self):
        # PositiveNumber пропускает 0, только отрицательные запрещены
        p = Product("Ноутбук", 50000, 0)
        assert p.quantity == 0

    def test_negative_price_raises(self):
        with pytest.raises(ValueError):
            Product("Ноутбук", -100, 10)

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError):
            Product("Ноутбук", 100, -1)

    def test_from_dict(self):
        p = Product.from_dict({"name": "Мышь", "price": 1500, "quantity": 20})
        assert p.name == "Мышь"
        assert p.price == 1500
        assert p.quantity == 20

    def test_calculate_discount_staticmethod(self):
        assert Product.calculate_discount(1000, 10) == 900

    def test_calculate_price_without_strategy(self, sample_product):
        assert sample_product.calculate_price() == sample_product.price

    def test_calculate_price_with_percent_discount(
        self, sample_product, percent_discount
    ):
        # 10% от 50000 → 45000
        assert sample_product.calculate_price(percent_discount) == 45000

    def test_calculate_price_with_fixed_discount(self, sample_product, fixed_discount):
        # 50000 - 500 → 49500
        assert sample_product.calculate_price(fixed_discount) == 49500

    def test_str_and_repr(self, sample_product):
        assert "Ноутбук" in str(sample_product)
        assert "Product" in repr(sample_product)

    def test_equality(self):
        assert Product("A", 100, 1) == Product("A", 100, 1)
        assert Product("A", 100, 1) != Product("B", 100, 1)

    def test_equality_with_other_type_returns_false(self, sample_product):
        assert (sample_product == "строка") is False

    def test_less_than(self):
        cheap = Product("Мышь", 1500, 1)
        expensive = Product("Ноутбук", 50000, 1)
        assert cheap < expensive

    def test_less_than_other_type_returns_notimplemented(self, sample_product):
        with pytest.raises(TypeError):
            sample_product < "строка"

    def test_to_json_returns_dict(self, sample_product):
        # Product.to_json переопределяет миксин и возвращает dict
        result = sample_product.to_json()
        assert isinstance(result, dict)
        assert result == {"name": "Ноутбук", "price": 50000, "quantity": 10}

    def test_to_dict_from_metaclass(self, sample_product):
        # ModelMeta добавляет to_dict() ко всем моделям
        d = sample_product.to_dict()
        assert d["name"] == "Ноутбук"


class TestDiscountStrategies:
    def test_percent_discount(self):
        assert PercentDiscount(10).apply(1000) == 900

    def test_percent_discount_zero(self):
        assert PercentDiscount(0).apply(1000) == 1000

    def test_fixed_discount(self):
        assert FixedDiscount(500).apply(1000) == 500

    def test_fixed_discount_more_than_price(self):
        # max(0, ...) — не уходим в минус
        assert FixedDiscount(2000).apply(1000) == 0


# ==================== User ====================


class TestUser:
    def test_create_user(self):
        u = User("Иван", "ivan@example.ru")
        assert u.name == "Иван"
        assert u.email == "ivan@example.ru"

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            User("Иван", "неверный_email")

    def test_get_info(self):
        u = User("Иван", "ivan@example.ru")
        info = u.get_info()
        assert "Иван" in info
        assert "ivan@example.ru" in info

    @pytest.mark.parametrize(
        "email",
        [
            "no-at-sign.ru",
            "no-domain@",
            "@no-local.ru",
            "плохой-email",
        ],
    )
    def test_invalid_emails(self, email):
        with pytest.raises(ValueError):
            User("Иван", email)

    @pytest.mark.parametrize(
        "email",
        [
            "a@b.ru",
            "user@example.com",
            "ivan.petrov@sfmshop.ru",
        ],
    )
    def test_valid_emails(self, email):
        u = User("Иван", email)
        assert u.email == email


# ==================== Order ====================


class TestOrder:
    def test_create_order(self, sample_user, sample_product):
        o = Order(user=sample_user, products=[sample_product])
        assert o.user is sample_user
        assert o.products == [sample_product]

    def test_calculate_total(self, sample_user):
        p1 = Product("Ноутбук", 50000, 1)
        p2 = Product("Мышь", 1500, 2)
        o = Order(user=sample_user, products=[p1, p2])
        # 50000*1 + 1500*2 = 53000
        assert o.calculate_total() == 53000

    def test_calculate_total_empty_order(self, sample_user):
        o = Order(user=sample_user, products=[])
        assert o.calculate_total() == 0

    def test_iter_returns_products(self, sample_user, sample_products):
        o = Order(user=sample_user, products=sample_products)
        assert list(o) == sample_products

    def test_eq_by_order_id(self, sample_user, sample_product):
        o1 = Order(sample_user, [sample_product], order_id=5)
        o2 = Order(sample_user, [sample_product], order_id=5)
        o3 = Order(sample_user, [sample_product], order_id=6)
        assert o1 == o2
        assert o1 != o3

    def test_eq_with_other_type(self, sample_order):
        assert (sample_order == "строка") is False

    def test_lt_by_created_at(self, sample_user, sample_product):
        from datetime import datetime

        o1 = Order(sample_user, [sample_product], created_at=datetime(2024, 1, 1))
        o2 = Order(sample_user, [sample_product], created_at=datetime(2024, 6, 1))
        assert o1 < o2

    def test_created_at_from_string(self, sample_user, sample_product):
        from datetime import datetime

        o = Order(sample_user, [sample_product], created_at="2024-01-15")
        assert o.created_at == datetime(2024, 1, 15)


class TestOrderCalculator:
    def test_calculate_total(self, sample_user, sample_products):
        o = Order(user=sample_user, products=sample_products)
        # 50000*1 + 1500*2 + 3000*1 = 56000
        assert OrderCalculator.calculate_total(o) == 56000

    def test_calculate_total_empty(self, sample_user):
        o = Order(user=sample_user, products=[])
        assert OrderCalculator.calculate_total(o) == 0

    def test_calculate_discount(self, sample_user):
        # Явно задаём quantity=1, чтобы не путаться
        p = Product("Ноутбук", 50000, 1)
        o = Order(user=sample_user, products=[p])
        # 50000 * (1 - 10/100) = 45000
        assert OrderCalculator.calculate_discount(o, 10) == 45000

    def test_calculate_discount_zero(self, sample_user):
        p = Product("Ноутбук", 50000, 1)
        o = Order(user=sample_user, products=[p])
        assert OrderCalculator.calculate_discount(o, 0) == 50000


class TestOrderValidator:
    def test_valid_order(self, sample_order):
        assert OrderValidator.validate(sample_order) is True

    def test_empty_products_raises(self, sample_user):
        o = Order(user=sample_user, products=[])
        with pytest.raises(ValueError, match="не может быть пустым"):
            OrderValidator.validate(o)

    def test_no_user_raises(self, sample_product):
        o = Order(user=None, products=[sample_product])
        with pytest.raises(ValueError, match="должен иметь пользователя"):
            OrderValidator.validate(o)

    def test_zero_quantity_raises(self, sample_user):
        # quantity=0 допустимо для Product, но не для заказа
        p = Product("Ноутбук", 50000, 0)
        o = Order(user=sample_user, products=[p])
        with pytest.raises(ValueError, match="Количество"):
            OrderValidator.validate(o)


# ==================== Descriptors ====================


class TestPositiveNumber:
    def test_zero_is_positive(self):
        class Dummy:
            value = PositiveNumber("_value")

            def __init__(self, v):
                self.value = v

        d = Dummy(0)
        assert d.value == 0

    def test_negative_raises(self):
        class Dummy:
            value = PositiveNumber("_value")

            def __init__(self, v):
                self.value = v

        with pytest.raises(ValueError):
            Dummy(-1)

    def test_class_access_returns_descriptor(self):
        class Dummy:
            value = PositiveNumber("_value")

        assert isinstance(Dummy.value, PositiveNumber)


# ==================== Exceptions ====================


class TestExceptions:
    def test_hierarchy(self):
        assert issubclass(InsufficientStockError, SFMShopException)
        assert issubclass(InvalidOrderError, SFMShopException)

    def test_negative_price_is_value_error(self):
        assert issubclass(NegativePriceError, ValueError)


# ==================== Mixins ====================


class TestMixins:
    def test_serializable_mixin_to_json(self):
        from src.models.mixins import SerializableMixin

        class Dummy(SerializableMixin):
            def __init__(self):
                self.x = 1
                self.y = "тест"

        result = Dummy().to_json()
        assert "Dummy" in result
        assert "тест" in result

    def test_loggable_mixin(self, capsys):
        from src.models.mixins import LoggableMixin

        class Dummy(LoggableMixin):
            pass

        Dummy().log("сообщение")
        captured = capsys.readouterr()
        assert "Dummy" in captured.out
        assert "сообщение" in captured.out
