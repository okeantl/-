import logging
from datetime import datetime

from pymongo import MongoClient

from src.core.config import settings

client = MongoClient(host=settings.mongo_host, port=settings.mongo_port)

db = client["sfmshop_logs"]
logs_collection = db["logs"]


def save_log(log_data):
    """Сохранение лога в MongoDB."""
    if "timestamp" not in log_data:
        log_data["timestamp"] = datetime.now()
    result = logs_collection.insert_one(log_data)
    return result.inserted_id


def get_all_logs():
    """Получение всех логов."""
    return list(logs_collection.find())


def get_logs_by_type(log_type):
    """Получение логов по типу."""
    return list(logs_collection.find({"type": log_type}))


class LogService:
    """Сервис логирования для проекта SFMShop."""

    def __init__(self, log_file: str = "app.log"):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def info(self, message: str, **kwargs):
        self.logger.info(f"{message} | {kwargs}")

    def error(self, message: str, **kwargs):
        self.logger.error(f"{message} | {kwargs}")

    def warning(self, message: str, **kwargs):
        self.logger.warning(f"{message} | {kwargs}")

    def critical(self, message: str, **kwargs):
        self.logger.critical(f"{message} | {kwargs}")


log_service = LogService()
logger = logging.getLogger(__name__)


def log_order_created(order_id: int):
    """Логирование создания заказа."""
    logger.info(f"Заказ создан: order_id={order_id}")


def log_order_error(error: str):
    """Логирование ошибки заказа."""
    logger.error(f"Ошибка обработки заказа: {error}")
