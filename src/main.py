# ==================
# УРОК 1: ПЕРЕМЕННЫЕ И СТРОКИ (STR)
# ==================

# Решение задачи от тимлида
company_name = "SFMShop"

welcome_message = "Добро пожаловать в " + company_name + "!"
slogan = company_name + " - лучший выбор для покупок"
email_subject = "Спасибо за покупку в " + company_name

print(welcome_message)
print(slogan)
print(email_subject)

# Практика: Задание 1 - Форматирование имен пользователей
raw_name_1 = "ИВАН"
raw_name_2 = "мария"
raw_name_3 = "пЕТР"

formatted_name_1 = raw_name_1.capitalize()
formatted_name_2 = raw_name_2.capitalize()
formatted_name_3 = raw_name_3.capitalize()

print(formatted_name_1)
print(formatted_name_2)
print(formatted_name_3)

# Практика: Задание 2 - Форматирование цены
price = "1999"

price_prefix = "от"
currency = "руб."

formatted_price = price_prefix + " " + price + " " + currency
print(formatted_price)

# ==================
# УРОК 2: ЧИСЛА (INT, FLOAT)
# ==================

# Решение задачи от тимлида - Конвертация валют
exchange_rate = 75.5  # Курс валюты

product_1_price_usd = 29.99
product_2_price_usd = 49.99
product_3_price_usd = 99.99

# Конвертируем в рубли и округляем
product_1_price_rub = round(product_1_price_usd * exchange_rate, 2)
product_2_price_rub = round(product_2_price_usd * exchange_rate, 2)
product_3_price_rub = round(product_3_price_usd * exchange_rate, 2)

print(product_1_price_rub)  # 2264.24
print(product_2_price_rub)  # 3774.25
print(product_3_price_rub)  # 7549.24

# Практика: Задание 1 - Расчет итоговой стоимости заказа
price_per_item = 1500.0
quantity = 3
discount = 0.1  # 10% скидка

# Расчет итоговой стоимости
final_price = price_per_item * quantity * (1 - discount)
final_price_rounded = round(final_price, 2)

print(final_price_rounded)

# Практика: Задание 2 - Сдача и купюры
paid = 5000  # сколько дал покупатель
cost = 3750  # стоимость заказа

change = paid - cost
notes = change // 500
rest = change % 500

print(f"Сдача: {change} руб; купюр по 500: {notes}, остаток: {rest} руб.")

# ==================
# УРОК 3: УСЛОВНЫЕ ОПЕРАТОРЫ
# ==================

# Решение задачи от тимлида - Проверка условий заказа
user_age = 20
product_quantity = 5

# Проверяем оба условия через and
if user_age >= 18 and product_quantity > 0:
    print("Заказ можно оформить")
else:
    # Определяем причину отказа
    if user_age < 18:
        print("Заказ нельзя оформить: пользователь несовершеннолетний")
    if product_quantity <= 0:
        print("Заказ нельзя оформить: товара нет на складе")

# Практика: Задание 1 - Определение размера скидки
order_total = 6000

if order_total > 10000:
    discount_rate = 0.15  # 15%
elif order_total > 5000:
    discount_rate = 0.10  # 10%
else:
    discount_rate = 0.05  # 5%

print("Размер скидки: " + str(discount_rate * 100) + "%")

# Практика: Задание 2 - Доступ пользователя
user_age = 17
user_balance = 500
order_total = 1000
requested_qty = 3
in_stock = 5

if user_age < 18:
    print("Отказ: пользователь несовершеннолетний")
elif user_balance < order_total:
    print("Отказ: недостаточно средств")
elif requested_qty > in_stock:
    print("Отказ: товара недостаточно на складе")
else:
    print("Заказ можно оформить")

# Практика: Задание 3 - Расчёт стоимости доставки
order_total = 3500
city = "Казань"

if order_total > 5000:
    delivery_cost = 0
elif city == "Москва" or city == "Санкт-Петербург":
    delivery_cost = 300
else:
    delivery_cost = 500

print("Стоимость доставки: " + str(delivery_cost) + " руб.")

# ==================
# УРОК 4: СПИСКИ (LIST)
# ==================

# Решение задачи от тимлида - Подсчет общей суммы заказов
orders = [1500, 2300, 890, 4500, 1200]

# Используем встроенные функции
total = sum(orders)
count = len(orders)
average = total / count

print("Общая сумма:", total)
print("Средний чек:", average)

# Практика: Задание 1 - Сортировка и поиск цен товаров
prices = [1500, 2300, 890, 4500, 1200]

# Сортируем по убыванию
prices.sort(reverse=True)

# Находим максимальную и минимальную цену
max_price = max(prices)
min_price = min(prices)

# Выводим результаты
print("Отсортированные цены:", prices)
print("Максимальная цена:", max_price)
print("Минимальная цена:", min_price)

# Практика: Задание 2 - Копирование списка заказов
orders = [1500, 2300, 890]

# Создаем копию для архива
archive = orders.copy()

# Добавляем новый заказ в оригинал
orders.append(4500)

# Проверяем, что архив не изменился
print("Текущие заказы:", orders)
print("Архив заказов:", archive)

# ==================
# УРОК 5: ЦИКЛЫ (FOR, WHILE)
# ==================

# Решение задачи от тимлида - Поиск заказов с суммой больше 5000
orders = [3000, 6000, 4500, 8000, 2000]

for order in orders:
    if order > 5000:
        print("Большой заказ:", order)

# Практика: Задание 1 - Поиск товаров с ценой больше 1000
prices = [500, 1500, 800, 2000, 1200]

# enumerate даёт номер (с нуля) и саму цену на каждом шаге
for i, price in enumerate(prices):
    # Номер товара для человека = индекс + 1
    if price > 1000:
        print("Товар " + str(i + 1) + ": " + str(price) + " руб.")

# Практика: Задание 2 - Сумма корзины со скидкой
prices = [500, 1500, 800, 2000, 1200]

total = 0
for price in prices:
    total += price

if total > 5000:
    total = total * 0.9

print(f"Итоговая сумма: {total} руб.")

# ==================
# УРОК 6: СЛОВАРИ (DICT) И МНОЖЕСТВА (SET)
# ==================

# Решение задачи от тимлида - Данные пользователя в словаре и уникальные посетители
# Хранение данных пользователя в словаре
user = {
    "name": "Иван Иванов",
    "email": "ivan@example.ru",
    "phone": "+7 999 123-45-67"
    }

# Получение данных по ключу
print("Имя:", user["name"])
print("Email:", user["email"])

# Подсчет уникальных посетителей через множество
visitors = {"user_123", "user_456", "user_123", "user_789"}
unique_count = len(visitors)

print("Уникальных посетителей:", unique_count)

# Практика: Задание 1 - Работа со словарем товара
product = {
    "name": "Ноутбук",
    "price": 50000,
    "quantity": 5
    }

# Обновляем количество
product["quantity"] = 10

# Получаем ключи и значения
keys = product.keys()
values = product.values()

print("Ключи словаря:", keys)
print("Значения словаря:", values)

# Практика: Задание 2 - Словарное включение из списка товаров
catalog = [["Ноутбук", 50000], ["Мышь", 1500], ["Клавиатура", 3000]]

# Создаем словарь через генератор
prices = {item[0]: item[1] for item in catalog}

print("Словарь цен:", prices)
print("Цена мыши:", prices.get("Мышь", 0))

# ==================
# УРОК 7: КОРТЕЖИ (TUPLE)
# ==================

# Решение задачи от тимлида - Хранение размеров товара в кортеже
# Хранение размеров в кортеже
dimensions = (30, 20, 15)

# Распаковка для расчета объема
length, width, height = dimensions
volume = length * width * height

print("Размеры товара:", dimensions)
print("Объем упаковки:", volume)

# Практика: Задание 1 - Работа с кортежами
# Создание кортежа с координатами
coordinates = (10, 20)

# Распаковка кортежа
x, y = coordinates

print("Координата x:", x)
print("Координата y:", y)

# Использование кортежа как ключа в словаре
locations = {
    (10, 20): "Офис",
    (30, 40): "Склад"
    }

# Получение названия места по координатам
location_name = locations[coordinates]
print("Название места:", location_name)

# Практика: Задание 2 - Распаковка координат склада
warehouse = (55, 37, "Москва")

lat, lon, city = warehouse

print(f"Склад в городе {city}: широта {lat}, долгота {lon}")

# ==================
# УРОК 8: ФУНКЦИИ
# ==================

# Решение задачи от тимлида - Валидация email и гибкое логирование
def validate_email(email):
    if "@" in email and "." in email:
        return True
    else:
        return False

# Проверка всех email через функцию
email_1 = "ivan@example.ru"
email_2 = "petr@test"
email_3 = "invalid-email"

result_1 = validate_email(email_1)
result_2 = validate_email(email_2)
result_3 = validate_email(email_3)

print("Email 1 валиден:", result_1)
print("Email 2 валиден:", result_2)
print("Email 3 валиден:", result_3)


def log_message(level, *args):
    # level - обязательный параметр (уровень лога)
    # args - любое количество данных для записи
    parts = []
    for item in args:
        parts.append(str(item))
    message = "[" + level + "] " + " ".join(parts)
    print(message)

# Разные варианты использования
log_message("INFO", "Пользователь зарегистрирован")
log_message("ERROR", "Ошибка валидации", "email", "petr@test")
log_message("DEBUG", "Проверка email", "ivan@example.ru", True)

# Практика: Задание 1 - Функция расчета цены со скидкой
def calculate_price_with_discount(price, discount_percent):
    final_price = price * (1 - discount_percent / 100)
    return final_price

# Вызов функции для разных товаров
price_1 = calculate_price_with_discount(1000, 10)
price_2 = calculate_price_with_discount(5000, 15)

print("Цена товара 1 со скидкой:", price_1)
print("Цена товара 2 со скидкой:", price_2)

# Практика: Задание 2 - Функция суммирования с *args
def sum_all(*args):
    total = 0
    for num in args:
        total = total + num
    return total

# Вызов с разным количеством аргументов
result_1 = sum_all(100, 200)
result_2 = sum_all(100, 200, 300, 400, 500)
result_3 = sum_all()

print("Сумма двух чисел:", result_1)
print("Сумма пяти чисел:", result_2)
print("Сумма без аргументов:", result_3)

# Практика: Задание 3 - Функция создания описания товара с **kwargs
def describe_product(name, **kwargs):
    parts = []
    for key in kwargs:
        parts.append(key + ": " + str(kwargs[key]))
    description = name + " (" + ", ".join(parts) + ")"
    return description

# Вызов с разным набором характеристик
info_1 = describe_product("Ноутбук", цена=50000, бренд="Lenovo", вес=2.1)
info_2 = describe_product("Мышь", цвет="черный")
info_3 = describe_product("Клавиатура")

print(info_1)
print(info_2)
print(info_3)

# ==================
# УРОК 8.5: ОСНОВЫ ИСКЛЮЧЕНИЙ (TRY/EXCEPT)
# ==================

# Решение задачи от тимлида - Безопасный расчет скидки и средней цены
def safe_calculate_discount(price, discount_percent):
    try:
        discount_amount = price * discount_percent / 100
        final_price = price - discount_amount
        return round(final_price, 2)
    except TypeError as error:
        print("Ошибка типа данных при расчете скидки: " + str(error))
        return None
    except ValueError as error:
        print("Ошибка значения при расчете скидки: " + str(error))
        return None


def calculate_average_price(prices):
    try:
        total = 0
        for price in prices:
            total = total + price
        average = total / len(prices)
        return round(average, 2)
    except ZeroDivisionError:
        print("Ошибка: список цен пуст, невозможно рассчитать среднюю цену")
        return 0
    except TypeError as error:
        print("Ошибка типа данных в списке цен: " + str(error))
        return 0

# Тестирование с корректными данными
price_with_discount = safe_calculate_discount(50000, 10)
print("Цена со скидкой: " + str(price_with_discount))

# Тестирование с неверным типом данных
price_error = safe_calculate_discount("не число", 10)
print("Результат при ошибке: " + str(price_error))

# Тестирование средней цены
average = calculate_average_price([50000, 1500, 3000, 25000])
print("Средняя цена: " + str(average))

# Тестирование с пустым списком
average_empty = calculate_average_price([])
print("Средняя цена (пустой список): " + str(average_empty))

# Практика: Задание 1 - Безопасный расчет стоимости заказа
def safe_order_total(items):
    total = 0
    processed_count = 0

    for item in items:
        try:
            item_total = item["price"] * item["quantity"]
            print(item["name"] + ": " + str(item_total) + " руб.")
        except KeyError:
            print("Ошибка в товаре " + item["name"] + ": отсутствует обязательное поле")
            continue
        except TypeError:
            print("Ошибка в товаре " + item["name"] + ": неверный тип данных для расчета")
            continue
        else:
            total = total + item_total
            processed_count = processed_count + 1

    print("Обработано товаров: " + str(processed_count) + " из " + str(len(items)))
    return total

# Тестовые данные
test_items = [
    {"name": "Ноутбук", "price": 50000, "quantity": 1},
    {"name": "Мышь", "price": 1500, "quantity": 2},
    {"name": "Клавиатура"},
    {"name": "Монитор", "price": None, "quantity": 1},
    {"name": "Наушники", "price": 3000, "quantity": 3}
    ]

result = safe_order_total(test_items)
print("Общая стоимость: " + str(result))

# Практика: Задание 2 - Валидация данных пользователя
def validate_user_data(user_data):
    errors_found = False

    # Проверка имени
    try:
        name = user_data["name"]
        if len(name) == 0:
            raise ValueError("имя не может быть пустым")
        print("Имя: OK")
    except KeyError:
        print("Имя: ошибка - поле отсутствует")
        errors_found = True
    except ValueError as error:
        print("Имя: ошибка - " + str(error))
        errors_found = True

    # Проверка возраста
    try:
        try:
            age = int(user_data["age"])
        except ValueError:
            raise ValueError("невозможно преобразовать в число")
        if age < 18 or age > 120:
            raise ValueError("возраст должен быть от 18 до 120")
        print("Возраст: OK (" + str(age) + ")")
    except KeyError:
        print("Возраст: ошибка - поле отсутствует")
        errors_found = True
    except ValueError as error:
        print("Возраст: ошибка - " + str(error))
        errors_found = True

    # Проверка email
    try:
        email = user_data["email"]
        if "@" not in email:
            raise ValueError("email должен содержать символ @")
        print("Email: OK")
    except KeyError:
        print("Email: ошибка - поле отсутствует")
        errors_found = True
    except ValueError as error:
        print("Email: ошибка - " + str(error))
        errors_found = True

    # Проверка телефона
    try:
        phone = user_data["phone"]
        clean_phone = phone.replace(" ", "").replace("-", "")
        # isdigit() - строковый метод: True, если в строке остались только цифры
        if not clean_phone.isdigit():
            raise ValueError("телефон должен содержать только цифры")
        print("Телефон: OK")
    except KeyError:
        print("Телефон: ошибка - поле отсутствует")
        errors_found = True
    except ValueError as error:
        print("Телефон: ошибка - " + str(error))
        errors_found = True

    if errors_found:
        print("Результат: найдены ошибки")
    else:
        print("Результат: все поля корректны")

    return not errors_found


# Тестовые данные
user_1 = {"name": "Иван Петров", "age": "25", "email": "ivan@sfmshop.ru", "phone": "89001234567"}
user_2 = {"name": "", "age": "молодой", "email": "неверный_email", "phone": "89oo1234567"}

print("Проверка пользователя 1:")
result_1 = validate_user_data(user_1)

print("")
print("Проверка пользователя 2:")
result_2 = validate_user_data(user_2)

# Практика: Задание 3 - Обработка корзины покупок
def add_to_cart(cart, name, price, quantity):
    try:
        if not name:
            raise ValueError("название товара не может быть пустым")
        if price <= 0 or quantity <= 0:
            raise ValueError("цена и количество должны быть положительными")
        item_total = price * quantity
        cart.append({"name": name, "total": item_total})
        print("Добавлен: " + name + " (" + str(price) + " руб. x " + str(quantity) + ")")
    except ValueError as error:
        print("Ошибка: " + str(error))
    except TypeError as error:
        print("Ошибка: неверный тип данных - " + str(error))


def remove_from_cart(cart, index):
    try:
        removed_item = cart.pop(index)
        print("Удален: " + removed_item["name"])
    except IndexError:
        print("Ошибка: товар с индексом " + str(index) + " не найден в корзине")


def get_cart_summary(cart):
    print("--- Корзина ---")
    try:
        total = 0
        item_number = 1
        for item in cart:
            print(str(item_number) + ". " + item["name"] + ": " + str(item["total"]) + " руб.")
            total = total + item["total"]
            item_number = item_number + 1
        print("Итого: " + str(total) + " руб. (товаров: " + str(len(cart)) + ")")
    except Exception as error:
        print("Ошибка при расчете корзины: " + str(error))

# Тестирование
cart = []
add_to_cart(cart, "Ноутбук", 50000, 1)
add_to_cart(cart, "Мышь", 1500, 2)
add_to_cart(cart, "", 3000, 1)
add_to_cart(cart, "Наушники", -500, 1)
remove_from_cart(cart, 1)
remove_from_cart(cart, 10)
get_cart_summary(cart)

# ==================
# УРОК 9: РАБОТА С ФАЙЛАМИ
# ==================

# Решение задачи от тимлида - Сохранение лога ошибок
error_message = "Ошибка: товар не найден на складе\n"

# Использование контекстного менеджера и режима 'a'
with open("data/errors.log", "a", encoding="utf-8") as file:
    file.write(error_message)
# Файл автоматически закрывается

# Практика: Задание 1 - Чтение и запись товаров
# Чтение товаров из файла
with open("data/products.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Обработка товаров и запись в новый файл
with open("data/products_with_prices.txt", "w", encoding="utf-8") as file:
    for line in lines:
        product = line.strip()  # Удаляем символ переноса строки
        product_with_price = product + " - 1000 руб.\n"
        file.write(product_with_price)

# Практика: Задание 2 - Подсчёт заказов в файле
with open("data/orders.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

orders = [line for line in lines if line.strip()]

print(f"Заказов в файле: {len(orders)}")

# ==================
# УРОК 10: ИМПОРТИРОВАНИЕ МОДУЛЕЙ, СОЗДАНИЕ СВОИХ МОДУЛЕЙ
# ==================

# Решение задачи от тимлида - Генерация промо-кода через модуль random
import random

promo_number = random.randint(100000, 999999)
promo_code = "PROMO" + str(promo_number)

print("Промо-код:", promo_code)

# Практика: Задание 1 - Создание модуля расчетов
from src.utils.calculations import calculate_discount

discount_1 = calculate_discount(1000, 0.1)
discount_2 = calculate_discount(5000, 0.15)

print("Скидка для товара 1:", discount_1)
print("Скидка для товара 2:", discount_2)

# Практика: Задание 2 - Функция скидки в отдельном модуле
import discounts

result = discounts.apply_discount(2000, 25)
print(f"Цена со скидкой: {result} руб.")

# ==================
# УРОК 11: ОБЛАСТИ ВИДИМОСТИ ПЕРЕМЕННЫХ
# ==================

# Решение задачи от тимлида - Глобальная константа стоимости доставки
# Глобальная константа определена в начале секции, до использования
BASE_DELIVERY_COST = 100

def calculate_order_total(price, quantity):
    # Используем глобальную константу (читаем, не изменяем)
    total = price * quantity + BASE_DELIVERY_COST
    return total

result = calculate_order_total(1000, 3)
print("Итого:", result)

# Практика: Задание 1 - Работа с глобальными переменными
# Глобальная переменная
DISCOUNT_RATE = 0.1

def calculate_price_with_global_discount(price):
    final_price = price * (1 - DISCOUNT_RATE)
    return final_price

# Первый вызов
price_1 = calculate_price_with_global_discount(1000)
print("Цена со скидкой 10%:", price_1)

# Изменение глобальной переменной
DISCOUNT_RATE = 0.2

# Второй вызов
price_2 = calculate_price_with_global_discount(1000)
print("Цена со скидкой 20%:", price_2)

# Практика: Задание 2 - Счётчик обработанных заказов
processed = 0

def handle_order():
    global processed
    processed += 1

handle_order()
handle_order()
handle_order()

print(f"Обработано заказов: {processed}")

# ==================
# УРОК 12: F-СТРОКИ, МЕТОДЫ СТРОК, ОТЛАДКА
# ==================

# Решение задачи от тимлида - Форматирование сообщения для лога через f-строку
order_id = 123
order_total = 5000
order_status = "новый"

# Использование f-строки вместо сложной конкатенации
message = f"Заказ #{order_id}, Сумма: {order_total} руб., Статус: {order_status}"
print(message)

# Практика: Задание 1 - Форматирование информации о товаре
def format_product_info(name, price, quantity):
    info = f"Товар: {name}, Цена: {price} руб., Количество: {quantity}"
    return info

# Использование функции
product_info = format_product_info("Ноутбук", 50000, 10)
print("Информация о товаре:", product_info)

# Обработка списка товаров
products = ["Ноутбук", "Мышь", "Клавиатура"]
products_string = ", ".join(products)
print(f"Товары: {products_string}")

# Практика: Задание 2 - Форматирование цены до копеек
price = 1234.5

print(f"Цена: {price:.2f} руб.")

# ==================
# УРОК 13: РАБОТА С ДАТАМИ И ВРЕМЕНЕМ
# ==================

# Решение задачи от тимлида - Расчет даты доставки через datetime и timedelta
from datetime import datetime, timedelta

# Создание объекта datetime
order_date = datetime.strptime("2024-01-15 10:00:00", "%Y-%m-%d %H:%M:%S")

# Расчет даты доставки
delivery_days = 3
delivery_date = order_date + timedelta(days=delivery_days)

print("Дата заказа:", order_date)
print("Дата доставки:", delivery_date)

# Практика: Задание 1 - Работа с датами
# Текущая дата и время
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print("Текущее время:", formatted_time)

# Даты заказа и доставки
order_date = datetime(2024, 1, 15, 10, 0, 0)
delivery_date = datetime(2024, 1, 18, 10, 0, 0)

print("Дата заказа:", order_date.strftime("%Y-%m-%d %H:%M:%S"))
print("Дата доставки:", delivery_date.strftime("%Y-%m-%d %H:%M:%S"))

# Разница между датами
difference = delivery_date - order_date
days = difference.days
print("Дней до доставки:", days)

# Практика: Задание 2 - Сколько дней до дедлайна
from datetime import date

start = date(2026, 12, 1)
deadline = date(2026, 12, 31)

delta = deadline - start
print(f"До дедлайна: {delta.days} дней")

# ==================
# УРОК 14: РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ
# ==================

# Решение задачи от тимлида - Надежная валидация email и телефона через regex
import re


def validate_email(email):
    pattern = r"[^@\s]+@[^@\s]+\.[^@\s]+"
    result = re.fullmatch(pattern, email)
    return result is not None


def validate_phone(phone):
    pattern = r"\+7[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    result = re.fullmatch(pattern, phone)
    return result is not None

email = "ivan@example.ru"
phone = "+7 999 123-45-67"

print("Email валиден:", validate_email(email))
print("Телефон валиден:", validate_phone(phone))

# Практика: Задание 1 - Валидация email через регулярное выражение
# Функция validate_email (через regex) уже объявлена выше, в решении задачи тимлида —
# второй раз её не объявляем, только проверяем разные адреса
email1 = "ivan@example.ru"
email2 = "invalid"
email3 = "test@"

print("Email '" + email1 + "' валиден:", validate_email(email1))
print("Email '" + email2 + "' валиден:", validate_email(email2))
print("Email '" + email3 + "' валиден:", validate_email(email3))

# Практика: Задание 2 - Извлечь все цены из текста
text = "Ноутбук 50000, мышь 800, клавиатура 1500"

prices = re.findall(r"\d+", text)
print(f"Найдены цены: {prices}")

# ==================
# УРОК 15: КЛАССЫ (ООП)
# ==================

# Решение задачи от тимлида - класс Product
# Класс лежит в src/models/product.py, здесь только используем его
from src.models.product import Product

laptop = Product("Ноутбук", 50000, 10)
total = laptop.get_total_price()
print("Общая стоимость:", total)

# Практика: Задание 1 - Классы User и Order
from src.models.user import User
from src.models.order import Order

user = User("Иван Иванов", "ivan@test.ru")
laptop = Product("Ноутбук", 50000, 1)
mouse = Product("Мышь", 1500, 2)
products = [laptop, mouse]
order = Order(user, products)

print(user.get_info())
print("Общая стоимость заказа:", order.calculate_total())

# Практика: Задание 2 - Валидация цены через @property
# Учебный класс в журнале: перекрывает импортированный Product до конца секции
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price  # Вызывает setter

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            print("Ошибка: цена не может быть отрицательной")
            return
        self._price = value

laptop = Product("Ноутбук", 50000)
print("Цена:", laptop.price)

laptop.price = -100
print("Цена после ошибки:", laptop.price)

# ==================
# УРОК 16: ПРИНЦИПЫ ООП
# ==================

# Решение задачи от тимлида - иерархия платежей
# (наследование, инкапсуляция, полиморфизм, абстракция)
class Payment:
    def __init__(self, amount):
        self.amount = amount

    def process_payment(self):
        raise NotImplementedError("Метод должен быть переопределен")


class CardPayment(Payment):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.__card_number = card_number  # Приватный атрибут

    def process_payment(self):
        # Доступ к приватному атрибуту только изнутри класса
        masked_card = "**** " + self.__card_number[-4:]
        return "Оплата картой " + masked_card + ": " + str(self.amount) + " руб."


class PayPalPayment(Payment):
    def __init__(self, amount, email):
        super().__init__(amount)
        self._email = email  # Защищенный атрибут

    def process_payment(self):
        return "Оплата PayPal (" + self._email + "): " + str(self.amount) + " руб."


# Использование полиморфизма: единый интерфейс для разных типов платежей
payments = [
    CardPayment(1000, "1234 5678 9012 3456"),
    PayPalPayment(2000, "user@paypal.com"),
]

for payment in payments:
    print(payment.process_payment())

# Практика: Задание 1 - Наследование
class Delivery:
    def get_description(self):
        return "Способ доставки"

class StandardDelivery(Delivery):
    def get_description(self):
        return "Стандартная доставка: 3-5 дней"

class ExpressDelivery(Delivery):
    def get_description(self):
        return "Экспресс-доставка: 1 день"

# Создание объектов
standard = StandardDelivery()
express = ExpressDelivery()

# Вызов методов
print(standard.get_description())
print(express.get_description())

# Практика: Задание 2 - Полиморфизм и инкапсуляция
class Product:
    def __init__(self, name, price):
        self.name = name
        self._price = price  # защищённый атрибут

    def final_price(self):
        return self._price


class DiscountProduct(Product):
    def __init__(self, name, price, discount):
        super().__init__(name, price)
        self.__discount = discount  # приватный атрибут

    def final_price(self):
        return self._price * (1 - self.__discount)


class GiftProduct(Product):
    def final_price(self):
        return 0


products = [
    Product("Кружка", 500),
    DiscountProduct("Футболка", 1000, 0.2),
    GiftProduct("Открытка", 300),
]

for product in products:
    print(product.name + ": " + str(product.final_price()) + " руб.")

# ==================
# УРОК 17: МАГИЧЕСКИЕ МЕТОДЫ
# ==================

# Решение задачи от тимлида - читаемый вывод и сравнение товаров
# В src/models/product.py добавлены __str__, __repr__, __lt__, __eq__
from src.models.product import Product

laptop = Product("Ноутбук", 50000, 10)
print(laptop)  # Товар: Ноутбук, Цена: 50000 руб., Количество: 10

products = [
    Product("Ноутбук", 50000, 10),
    Product("Мышь", 1500, 20),
    Product("Клавиатура", 3000, 15),
]
products.sort()  # сортировка по цене через __lt__
for product in products:
    print(product)

# Практика: Задание 1 - Добавление __str__ и __repr__
# Методы уже написаны в решении задачи тимлида, здесь только проверка
laptop = Product("Ноутбук", 50000, 10)
print(laptop)
print(repr(laptop))

# Практика: Задание 2 - Корзина с __len__ и __add__
class Cart:
    def __init__(self, owner, items):
        self.owner = owner
        self.items = items

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        return Cart(self.owner, self.items + other.items)

    def __str__(self):
        return "Корзина " + self.owner + ": " + str(len(self)) + " товаров на " + str(sum(self.items)) + " руб."

cart1 = Cart("Иван", [50000, 1500])
cart2 = Cart("Иван", [3000, 2500])

print(len(cart1))
merged = cart1 + cart2
print(len(merged))
print(merged)

# ==================
# УРОК 18: ОБРАБОТКА ИСКЛЮЧЕНИЙ (TRY/EXCEPT, RAISE)
# ==================

# Решение задачи от тимлида - валидация через raise и обработка через try/except
# Проверки добавлены в src/models/product.py и src/models/user.py
from src.models.product import Product
from src.models.user import User

try:
    product = Product("Ноутбук", -50000, 10)
except ValueError as e:
    print("Ошибка при создании товара:", e)
    product = Product("Ноутбук", 0, 10)  # Создаем с корректными данными

try:
    user = User("Иван", "неверный_email")
except ValueError as e:
    print("Ошибка при создании пользователя:", e)
    user = User("Иван", "default@example.ru")

# Практика: Задание 1 - Обработка ошибок деления
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
        return None
    except TypeError:
        print("Ошибка: неверный тип данных!")
        return None

# Тестирование
print("Результат:", divide(10, 2))
print(divide(10, 0))
print(divide("10", 2))

# Практика: Задание 2 - Резервирование товара со складскими исключениями
class OutOfStockError(Exception):
    pass


class Order:
    def __init__(self, product_name, stock):
        self.product_name = product_name
        self.stock = stock

    def reserve(self, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")
        if quantity > self.stock:
            raise OutOfStockError(
                f"Недостаточно товара: запрошено {quantity}, в наличии {self.stock}"
            )
        self.stock -= quantity
        return self.stock


order = Order("Ноутбук", 5)

requests = [3, 10, 0]
for qty in requests:
    try:
        remaining = order.reserve(qty)
        print(f"Зарезервировано {qty}, осталось {remaining}")
    except OutOfStockError as e:
        print("Нет на складе:", e)
    except ValueError as e:
        print("Ошибка ввода:", e)

# ==================
# УРОК 19: СОЗДАНИЕ СОБСТВЕННЫХ ИСКЛЮЧЕНИЙ
# ==================

# Решение задачи от тимлида и Задание 1 - в файлах src/models/exceptions.py и src/models/product.py
# (проверка в REPL, в журнал не пишем)

# Практика: Задание 2 - Иерархия исключений склада
class SFMShopException(Exception):
    """Базовое исключение проекта SFMShop"""
    pass


class InsufficientStockError(SFMShopException):
    """Товара недостаточно на складе"""
    pass


class InvalidQuantityError(SFMShopException):
    """Некорректное количество товара"""
    pass


class Product:
    def __init__(self, name, stock):
        self.name = name
        self.stock = stock

    def sell(self, amount):
        if amount <= 0:
            raise InvalidQuantityError(
                f"Количество должно быть больше нуля, получено: {amount}"
            )
        if self.stock < amount:
            raise InsufficientStockError(
                f"Товара недостаточно. На складе: {self.stock}, требуется: {amount}"
            )
        self.stock -= amount
        return self.stock


def process_order(product, amount):
    try:
        left = product.sell(amount)
        print(f"Продано {amount} шт. товара '{product.name}'. Остаток: {left}")
    except InsufficientStockError as e:
        print("Ошибка склада:", e)
    except SFMShopException as e:
        print("Ошибка проекта:", e)


product = Product("Ноутбук", 10)
process_order(product, 3)
process_order(product, 100)
process_order(product, -5)
process_order(product, 7)

# ==================
# УРОК 28: HTTP-ЗАПРОСЫ И ОТВЕТЫ
# ==================

# Практика: Задание 2 - Мини-роутер запросов SFMShop
from http import HTTPStatus

# Каталог товаров SFMShop (in-memory)
PRODUCTS = {
    1: {"id": 1, "name": "Ноутбук", "price": 50000},
    2: {"id": 2, "name": "Мышь", "price": 1500},
}


def handle_request(method, path):
    """Возвращает кортеж (числовой статус, текстовая причина, тело-строка)
    по HTTP-методу и пути. Реализует endpoint'ы SFMShop."""

    # GET /products - список товаров
    if method == "GET" and path == "/products":
        names = ", ".join(p["name"] for p in PRODUCTS.values())
        status = HTTPStatus.OK
        return (status.value, status.phrase, names)

    # GET /products/{id} - товар по ID
    if method == "GET" and path.startswith("/products/"):
        pid = int(path.split("/")[-1])
        if pid in PRODUCTS:
            status = HTTPStatus.OK
            return (status.value, status.phrase, PRODUCTS[pid]["name"])
        status = HTTPStatus.NOT_FOUND
        return (status.value, status.phrase, f"Товар с id={pid} не найден")

    # POST /orders - создание заказа
    if method == "POST" and path == "/orders":
        status = HTTPStatus.CREATED
        return (status.value, status.phrase, "Заказ создан")

    # DELETE /products/{id} - удаление товара
    if method == "DELETE" and path.startswith("/products/"):
        pid = int(path.split("/")[-1])
        if pid in PRODUCTS:
            status = HTTPStatus.OK
            return (status.value, status.phrase, "Товар удалён")
        status = HTTPStatus.NOT_FOUND
        return (status.value, status.phrase, f"Товар с id={pid} не найден")

    # Метод/путь не поддерживается endpoint'ом
    status = HTTPStatus.NOT_FOUND
    return (status.value, status.phrase, "Endpoint не найден")


sample_requests = [
    ("GET", "/products"),
    ("GET", "/products/1"),
    ("GET", "/products/999"),
    ("POST", "/orders"),
    ("DELETE", "/products/2"),
]

for method, path in sample_requests:
    code, phrase, body = handle_request(method, path)
    print(f"{method} {path} -> {code} {phrase} | {body}")
