from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    database_url: str = "sqlite:///./sfmshop.db"

    # Опционально -- только если подключаешь YandexGPT
    yandex_api_key: str = ""
    yandex_folder_id: str = ""

    # Урок «Переменные окружения»: остальная конфигурация тоже из окружения
    secret_key: str = ""
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    max_connections: int = 10

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
