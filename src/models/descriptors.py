class PositiveNumber:
    """Дескриптор для валидации положительных чисел"""

    def __init__(self, name):
        """Инициализация дескриптора"""
        self.name = name # Имя атрибута для хранения значения

    def __get__(self, instance, owner):
        """Получение значения"""
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        """Установка значения с валидацией"""
        if value < 0:
            raise ValueError(f"{self.name} не может быть отрицательным")
        setattr(instance, self.name, value)
