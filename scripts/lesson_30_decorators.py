def log_call(func):
    """Декоратор: логирует вызов функции с аргументами"""

    def wrapper(*args, **kwargs):
        args_str = ", ".join(str(a) for a in args)
        print(f"Вызов: {func.__name__}({args_str})")
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_call
def calculate_order(price, quantity, discount):
    """Рассчитать стоимость заказа со скидкой"""
    return price * quantity * (1 - discount)

# Используем функцию - декоратор автоматически логирует вызовы
result_1 = calculate_order(1000, 3, 0.1)
result_2 = calculate_order(2000, 1, 0.2)

print(f"Заказ 1: {result_1} руб.")
print(f"Заказ 2: {result_2} руб.")
