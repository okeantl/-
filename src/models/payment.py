from abc import ABC, abstractmethod


class Payment(ABC):
    """Абстрактный класс для платежей"""

    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def process(self):
        """Общая часть обработки платежа.

        Метод абстрактный: создать Payment(...) напрямую нельзя, наследник
        обязан переопределить process(). Но тело у него есть — наследники
        вызывают его через super().process() (урок 35 «MRO»).
        """
        print(f"Базовая обработка платежа на {self.amount}")


class Loggable:
    """Миксин: умеет писать в лог"""

    def log(self, message):
        print(f"[LOG] {message}")


class Refundable:
    """Миксин: умеет возвращать деньги"""

    def refund(self, amount):
        print(f"Возврат {amount} на счёт")


class CardPayment(Payment, Loggable, Refundable):
    """Оплата картой: платёж + лог + возврат (урок 35 «MRO»)"""

    def process(self):
        self.log("начало платежа")
        super().process()  # по MRO: следующий класс, у которого есть process, — Payment
        return True


class PayPalPayment(Payment):
    """Оплата через PayPal"""

    def process(self):
        print(f"Оплата {self.amount} руб. через PayPal")
        return True


# Использование
def process_payment(payment: Payment):
    """Обработка платежа - работает с любым типом Payment"""
    return payment.process()


if __name__ == "__main__":
    # Порядок поиска методов: CardPayment -> Payment -> ABC -> Loggable -> Refundable -> object
    print([cls.__name__ for cls in CardPayment.mro()])

    p = CardPayment(1000)
    p.process()
    p.refund(500)
