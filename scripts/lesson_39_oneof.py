class OneOf:
    """Дескриптор: разрешает только значения из заданного набора"""

    def __init__(self, *allowed):
        self.allowed = set(allowed)

    def __set_name__(self, owner, name):
        # Python сам передаёт сюда имя поля при объявлении класса
        self.storage_name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value not in self.allowed:
            allowed_str = ", ".join(sorted(self.allowed))
            raise ValueError(f"Недопустимое значение: {value}. Разрешено: {allowed_str}")
        setattr(instance, self.storage_name, value)


class Order:
    status = OneOf("new", "paid", "shipped", "cancelled")

    def __init__(self, order_id, status):
        self.order_id = order_id
        self.status = status


order = Order(1, "new")
print(order.status)

order.status = "paid"
print(order.status)

try:
    order.status = "deleted"
except ValueError as e:
    print(f"Ошибка: {e}")
