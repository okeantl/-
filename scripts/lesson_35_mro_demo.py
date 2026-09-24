class Payment:
    def process(self):
        print("Payment.process()")


class Loggable:
    def log(self):
        print("Loggable.log()")


class CardPayment(Payment, Loggable):
    def process(self):
        print("CardPayment.process()")
        self.log()  # Вызовет Loggable.log() (второй родитель в MRO)
        super().process()  # Вызовет Payment.process() (первый родитель в MRO)


if __name__ == "__main__":
    # Просмотр MRO
    print("MRO для CardPayment:")
    for i, cls in enumerate(CardPayment.mro(), 1):
        print(f"{i}. {cls.__name__}")

    # Использование
    payment = CardPayment()
    payment.process()
