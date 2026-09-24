import os


def load_config():
    return {
        "DATABASE_URL": os.environ.get("DATABASE_URL", "postgresql://localhost:5432/sfmshop"),
        "DEBUG": os.environ.get("DEBUG", "False").lower() == "true",
        "MAX_CONNECTIONS": int(os.environ.get("MAX_CONNECTIONS", "10")),
        "ENVIRONMENT": os.environ.get("ENVIRONMENT", "development"),
    }


if __name__ == "__main__":
    # Эмулируем окружение production
    os.environ["ENVIRONMENT"] = "production"
    os.environ["DATABASE_URL"] = "postgresql://prod-server:5432/sfmshop"
    os.environ["DEBUG"] = "False"
    os.environ["MAX_CONNECTIONS"] = "50"

    config = load_config()

    print(f"ENVIRONMENT: {config['ENVIRONMENT']}")
    print(f"DATABASE_URL: {config['DATABASE_URL']}")
    print(f"DEBUG: {config['DEBUG']}")
    print(f"MAX_CONNECTIONS: {config['MAX_CONNECTIONS']}")
    print(f"DEBUG type: {type(config['DEBUG']).__name__}")
    print(f"MAX_CONNECTIONS type: {type(config['MAX_CONNECTIONS']).__name__}")

    # Проверяем значения по умолчанию (переменная REDIS_URL не задана)
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    print(f"REDIS_URL (default): {redis_url}")
