import time
from typing import Optional

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

from src.core.config import settings


class ExchangeClient:
    """Клиент для работы с API курсов валют."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.exchange_api_url
        self.timeout = 5
        self.max_retries = 3

    def get_exchange_rate(
        self,
        base_currency: str,
        target_currency: str,
    ) -> Optional[float]:
        """Получить курс валют с обработкой ошибок и retry."""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    f"{self.base_url}/{base_currency}",
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()

                if target_currency in data.get("rates", {}):
                    return data["rates"][target_currency]
                print(f"Валюта {target_currency} не найдена")
                return None

            except Timeout:
                if attempt < self.max_retries - 1:
                    delay = 2**attempt
                    print(f"Таймаут, повтор через {delay} сек...")
                    time.sleep(delay)
                else:
                    print("Превышено время ожидания")
                    return None

            except ConnectionError:
                if attempt < self.max_retries - 1:
                    delay = 2**attempt
                    print(f"Ошибка подключения, повтор через {delay} сек...")
                    time.sleep(delay)
                else:
                    print("Ошибка подключения")
                    return None

            except RequestException as e:
                print(f"Ошибка запроса: {e}")
                return None
        return None
