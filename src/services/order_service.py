# Архитектура системы с брокером сообщений для проекта SFMShop:
#
# Компоненты:
# 1. Producer (src/api/main.py):
# - При создании заказа через POST /orders отправляет задачи в очередь
# - Задачи отправляются быстро, API отвечает сразу
# - Не блокирует ответ пользователю
#
# 2. Очередь сообщений (RabbitMQ):
# - Хранит задачи для обработки
# - Обеспечивает надежность доставки (сообщения не теряются)
# - Поддерживает приоритеты задач
# - Гарантирует порядок обработки
#
# 3. Consumer (src/services/queue_consumer.py):
# - Получает задачи из очереди
# - Обрабатывает задачи в фоне
# - Обрабатывает ошибки и retry (3 попытки)
# - Может масштабироваться (несколько воркеров)
#
# Задачи для очереди:
# - send_email: отправка email-уведомлений пользователю
# - update_stock: обновление количества товаров на складе
# - generate_report: генерация отчетов по заказам
# - send_notification: отправка push-уведомлений
#
# Преимущества:
# - Быстрый ответ API (не ждет выполнения задач)
# - Масштабируемость (можно запустить несколько Consumer)
# - Надежность (сообщения не теряются, retry при ошибках)
# - Разделение ответственности (API и обработка задач разделены)

from src.database.models import Order
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository


class InsufficientStockError(Exception):
    """Недостаточно товара на складе."""

    pass


class OrderService:
    """Сервис для работы с заказами."""

    # Минимальное количество для оптовой скидки
    BULK_DISCOUNT_THRESHOLD = 10
    BULK_DISCOUNT_RATE = 0.9

    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        ):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def create_order(
        self,
        user_id: int,
        product_id: int,
        quantity: int,
        ) -> Order:
        """Создать заказ с проверкой остатков и расчётом скидки."""
        product = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Товар {product_id} не найден")

        if product.quantity < quantity:
            raise InsufficientStockError(
                f"На складе {product.quantity} шт., запрошено {quantity}"
                )

        total = self._calculate_total(product.price, quantity)

        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total=total,
            )
        order = await self.order_repo.create(order)

        # Списываем остатки
        await self.product_repo.update_stock(product_id, -quantity)

        return order

    def _calculate_total(self, price: float, quantity: int) -> float:
        """Расчёт стоимости с учётом оптовой скидки."""
        # price из ORM-модели приходит как Decimal (Numeric) -- приводим к float
        total = float(price) * quantity
        if quantity >= self.BULK_DISCOUNT_THRESHOLD:
            total *= self.BULK_DISCOUNT_RATE
        return total

    async def cancel_order(self, order_id: int) -> Order:
        """Отменить заказ и вернуть товар на склад."""
        order = await self.order_repo.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Заказ {order_id} не найден")

        if order.status == "cancelled":
            raise ValueError("Заказ уже отменён")

        order.status = "cancelled"

        # Возвращаем товар на склад
        await self.product_repo.update_stock(
            order.product_id,
            order.quantity,
            )

        return order

    async def get_order(self, order_id: int) -> Order | None:
        """Получить заказ по ID (эндпоинт GET /orders/{order_id})."""
        return await self.order_repo.get_by_id(order_id)
