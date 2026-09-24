from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Единая конфигурация SFMShop. Все значения читаются из .env."""

    # --- Основная БД ---
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "sfmshop"
    db_user: str = "postgres"
    db_password: str = ""

    # --- Реплика для чтения ---
    db_primary_host: str = "localhost"
    db_replica_host: str = "localhost"
    db_replica_port: int = 5432

    # --- Mongo (логи) ---
    mongo_host: str = "localhost"
    mongo_port: int = 27017

    # --- Redis ---
    redis_url: str = "redis://localhost:6379"

    # --- Rate limits ---
    rate_limit_login: str = "5/minute"
    rate_limit_products: str = "30/minute"

    # --- CORS ---
    cors_origins: str = "http://localhost:3000"

    # --- Общие ---
    database_url: str = "postgresql://user:password@localhost:5432/sfmshop"
    secret_key: str = ""
    debug: bool = False
    max_connections: int = 10

    # --- Внешние API ---
    anthropic_api_key: str = ""
    exchange_api_url: str = "https://api.exchangerate-api.com/v4/latest"

    # --- Опционально: YandexGPT ---
    yandex_api_key: str = ""
    yandex_folder_id: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
