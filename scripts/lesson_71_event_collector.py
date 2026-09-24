import logging
from collections import Counter


class EventCollector(logging.Handler):
    """Хендлер, который копит записи логов в памяти для анализа."""

    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def setup_logger():
    """Создать логгер SFMShop с коллектором событий."""
    logger = logging.getLogger("sfmshop")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    collector = EventCollector()
    logger.addHandler(collector)
    return logger, collector


def log_shop_events(logger):
    """Залогировать события магазина."""
    logger.info("Заказ создан: order_id=101")
    logger.warning("Медленный ответ БД при заказе order_id=102")
    logger.error("Ошибка оплаты: order_id=103")
    logger.info("Заказ создан: order_id=104")
    logger.error("Ошибка склада: товар отсутствует")


def build_report(collector):
    """Посчитать события по уровням важности."""
    counts = Counter(record.levelname for record in collector.records)
    return counts


def main():
    logger, collector = setup_logger()
    log_shop_events(logger)
    report = build_report(collector)

    print("Отчёт по событиям:")
    for level in ("INFO", "WARNING", "ERROR"):
        print(f"{level}: {report.get(level, 0)}")
    print(f"Всего событий: {len(collector.records)}")

    problems = [
        r.getMessage() for r in collector.records
        if r.levelno >= logging.ERROR
    ]
    print("Проблемные события:")
    for msg in problems:
        print(f"- {msg}")


if __name__ == "__main__":
    main()
