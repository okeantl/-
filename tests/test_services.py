from unittest.mock import MagicMock, patch

from src.services.exchange_client import ExchangeClient


@patch('src.services.exchange_client.requests.get')
def test_get_exchange_rate(mock_get):
    """Тест: курс берётся из ответа внешнего API, сети нет"""
    # Настройка мока: подменяем ответ внешнего сервиса
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 92.5, "EUR": 0.92}}
    mock_get.return_value = mock_response

    rate = ExchangeClient().get_exchange_rate("USD", "RUB")

    # Проверка результата
    assert rate == 92.5
    # Проверка, что запрос был сделан по нужному адресу
    mock_get.assert_called_once_with(
        "https://api.exchangerate-api.com/v4/latest/USD", timeout=5
    )


@patch('src.services.exchange_client.requests.get')
def test_get_exchange_rate_unknown_currency(mock_get):
    """Тест: валюты нет в ответе - клиент возвращает None"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"EUR": 0.92}}
    mock_get.return_value = mock_response

    assert ExchangeClient().get_exchange_rate("USD", "XYZ") is None
