import logging
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Подключение к MongoDB
client = MongoClient(
    host=os.getenv('MONGO_HOST', 'localhost'),
    port=int(os.getenv('MONGO_PORT', 27017))
    )

db = client['sfmshop_logs']
logs_collection = db['logs']


def save_log(log_data):
    """Сохранение лога в MongoDB"""
    if 'timestamp' not in log_data:
        log_data['timestamp'] = datetime.now()

    result = logs_collection.insert_one(log_data)
    return result.inserted_id


def get_all_logs():
    """Получение всех логов"""
    logs = logs_collection.find()
    return list(logs)


def get_logs_by_type(log_type):
    """Получение логов по типу"""
    logs = logs_collection.find({"type": log_type})
    return list(logs)

# Сервис логирования SFMShop (урок «Логирование и мониторинг»)
class LogService:
    """Сервис логирования для проекта SFMShop"""

    def __init__(self, log_file: str = 'app.log'):
        """Инициализация сервиса логирования"""
        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
            ]
            )

        self.logger = logging.getLogger(__name__)

    def info(self, message: str, **kwargs):
        """Логирование информационного сообщения"""
        self.logger.info(f"{message} | {kwargs}")

    def error(self, message: str, **kwargs):
        """Логирование ошибки"""
        self.logger.error(f"{message} | {kwargs}")

    def warning(self, message: str, **kwargs):
        """Логирование предупреждения"""
        self.logger.warning(f"{message} | {kwargs}")

    def critical(self, message: str, **kwargs):
        """Логирование критической ошибки"""
        self.logger.critical(f"{message} | {kwargs}")
        # Можно добавить отправку алерта


# Глобальный экземпляр
log_service = LogService()


# Логирование событий заказа (задание 1): настройку уже сделал LogService
logger = logging.getLogger(__name__)


def log_order_created(order_id: int):
    """Логирование создания заказа"""
    logger.info(f"Заказ создан: order_id={order_id}")


def log_order_error(error: str):
    """Логирование ошибки заказа"""
    logger.error(f"Ошибка обработки заказа: {error}")


# Тестирование
if __name__ == "__main__":
    # Вставка лога ошибки
    error_log = {
        "type": "error",
        "message": "Ошибка подключения к БД",
        "stack_trace": "Traceback (most recent call last)...",
        "timestamp": datetime.now()
        }
    error_id = save_log(error_log)
    print(f"Лог ошибки сохранен: {error_id}")

    # Вставка лога доступа
    access_log = {
        "type": "access",
        "ip": "192.168.1.1",
        "endpoint": "/api/products",
        "method": "GET",
        "status_code": 200,
        "timestamp": datetime.now()
        }
    access_id = save_log(access_log)
    print(f"Лог доступа сохранен: {access_id}")

    # Поиск всех логов
    all_logs = get_all_logs()
    print(f"Всего логов: {len(all_logs)}")

    # Поиск логов по типу
    error_logs = get_logs_by_type("error")
    print(f"Логов ошибок: {len(error_logs)}")
