import time
import uuid

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel


router = APIRouter(tags=["background"])


def send_confirmation_email(order_id: int, email: str):
    """Отправка email подтверждения (выполняется в фоне)"""
    time.sleep(3)  # Имитация работы с SMTP
    print(f"Email отправлен на {email} для заказа #{order_id}")


@router.post("/orders/{order_id}/confirm")
async def confirm_order(order_id: int, background_tasks: BackgroundTasks):
    """Подтверждение заказа — ответ мгновенный"""
    email = "customer@sfmshop.ru"  # В реальности — из БД

    background_tasks.add_task(send_confirmation_email, order_id, email)

    return {"order_id": order_id, "status": "confirmed"}


task_statuses: dict[str, dict] = {}


def export_catalog(task_id: str):
    """Экспорт каталога товаров (выполняется в фоне)"""
    task_statuses[task_id] = {"status": "in_progress"}
    try:
        time.sleep(10) # Имитация формирования файла
        task_statuses[task_id] = {
            "status": "completed",
            "result": {"file": "catalog_export.csv", "rows": 1500},
            }
    except Exception as e:
        task_statuses[task_id] = {"status": "failed", "error": str(e)}


@router.post("/exports")
async def start_export(background_tasks: BackgroundTasks):
    """Запуск экспорта каталога"""
    task_id = str(uuid.uuid4())
    task_statuses[task_id] = {"status": "pending"}

    background_tasks.add_task(export_catalog, task_id)

    return {"task_id": task_id, "status": "accepted"}


@router.get("/exports/{task_id}")
async def get_export_status(task_id: str):
    """Проверка статуса экспорта"""
    if task_id not in task_statuses:
        return {"error": "Задача не найдена"}
    return {"task_id": task_id, **task_statuses[task_id]}


class BackgroundOrderCreate(BaseModel):
    user_email: str
    items: list[dict]
    total: float


def send_email(order_id: int, email: str):
    """Отправка email подтверждения"""
    time.sleep(3)
    print(f"Email отправлен на {email} для заказа #{order_id}")


def update_stock(order_id: int, items: list[dict]):
    """Обновление остатков на складе"""
    time.sleep(2)
    for item in items:
        print(f"Заказ #{order_id}: остаток обновлён для товара {item['product_id']}")


def notify_manager(order_id: int, total: float):
    """Уведомление менеджера о новом заказе"""
    time.sleep(1)
    print(f"Менеджер уведомлён: заказ #{order_id} на сумму {total} руб.")


@router.post("/orders/background")
async def create_order(order: BackgroundOrderCreate, background_tasks: BackgroundTasks):
    """Создание заказа с тремя фоновыми задачами"""
    order_id = 42  # В реальности — сохранение в БД

    background_tasks.add_task(send_email, order_id, order.user_email)
    background_tasks.add_task(update_stock, order_id, order.items)
    background_tasks.add_task(notify_manager, order_id, order.total)

    return {"order_id": order_id, "status": "processing"}
