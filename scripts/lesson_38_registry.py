class RegistryMeta(type):
    """Метакласс, который автоматически регистрирует классы моделей в реестре"""
    _registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if name != "Model":
            cls._registry[name] = new_class
        return new_class


class Model(metaclass=RegistryMeta):
    pass


class Product(Model):
    def __init__(self, name, price, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity


class Order(Model):
    def __init__(self, user, products):
        self.user = user
        self.products = products


class User(Model):
    def __init__(self, login):
        self.login = login


for model_name in sorted(RegistryMeta._registry):
    print(model_name)

print("Всего моделей:", len(RegistryMeta._registry))
print("Order зарегистрирован:", "Order" in RegistryMeta._registry)
print("Model в реестре:", "Model" in RegistryMeta._registry)
