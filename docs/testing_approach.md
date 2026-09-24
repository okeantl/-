# Подход к тестированию в проекте SFMShop

## Обзор

В проекте SFMShop используется модульное тестирование для проверки критичной бизнес-логики. Покрытие кода тестами составляет более 80% для критичных компонентов.

## Типы тестов

### Unit-тесты
- **Файлы**: `tests/test_utils.py`
- **Покрытие**: функции расчёта из `src/utils/calculations.py` — `calculate_discount`, `calculate_delivery`
- **Инструменты**: pytest, параметризация

### Integration-тесты
- **Файлы**: `tests/test_api.py`
- **Покрытие**: эндпоинты `GET /products` и `POST /orders`
- **Особенности**: внешние сервисы изолированы моками

## Инструменты и практики

### Инструменты
- **pytest** - для написания и запуска тестов
- **pytest-cov** - для проверки покрытия кода
- **unittest.mock** - для моков и изоляции тестов

### Практики
- **TDD** - разработка через тестирование для новых функций
- **Фикстуры** - для подготовки тестовых данных
- **Параметризация** - для проверки разных случаев
- **Моки** - для изоляции от внешних зависимостей

## Покрытие кода

- **Критичная бизнес-логика**: >80%
- **Функции расчета**: 100%
- **API endpoints**: >70%

## Примеры тестов

### Unit-тест функции

    def test_calculate_discount():
        assert calculate_discount(1000, 0.05) == 50

### Integration-тест API

    @patch('src.database.queries.create_order')
    def test_create_order(mock_create_order):
        mock_create_order.return_value = 5
        response = client.post("/orders", json={"user_id": 1, "product_id": 2, "quantity": 1})
        assert response.status_code == 200

## Запуск тестов

    # Запуск всех тестов
    pytest

    # Запуск с проверкой покрытия
    pytest --cov=src --cov-report=html

    # Запуск конкретного файла
    pytest tests/test_utils.py
