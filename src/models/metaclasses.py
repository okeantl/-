class ModelMeta(type):
    """Метакласс для автоматического добавления методов"""

    def __new__(cls, name, bases, attrs):
        """Вызывается при создании класса"""
        # Добавить метод to_dict() ко всем классам моделей
        def to_dict(self):
            """Преобразовать объект в словарь"""
            return self.__dict__

        # Не перекрывать to_dict(), который класс или его базы определили сами
        if "to_dict" not in attrs and not any(hasattr(base, "to_dict") for base in bases):
            attrs["to_dict"] = to_dict

        # Создать класс
        return super().__new__(cls, name, bases, attrs)
