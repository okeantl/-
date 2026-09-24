import asyncio
import random


async def order_producer(queue: asyncio.Queue, num_orders: int, num_workers: int):
    """Генерация заказов"""
    for i in range(num_orders):
        order = {
            "id": i + 1,
            "total": random.randint(500, 10000),
            "items": random.randint(1, 5),
        }
        await queue.put(order)
        print(f"Новый заказ #{order['id']} — {order['total']} руб.")
        await asyncio.sleep(0.3)

    # Сигнал завершения для каждого worker
    for _ in range(num_workers):
        await queue.put(None)


async def order_worker(name: str, queue: asyncio.Queue):
    """Обработка заказов из очереди"""
    processed = 0
    while True:
        order = await queue.get()

        if order is None:
            print(f"Worker {name}: завершение (обработано {processed} заказов)")
            break

        # Имитация обработки
        processing_time = order["items"] * 0.3
        print(f"Worker {name}: обработка заказа #{order['id']}...")
        await asyncio.sleep(processing_time)
        print(f"Worker {name}: заказ #{order['id']} готов")

        processed += 1
        queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=5)
    num_workers = 3
    num_orders = 10

    await asyncio.gather(
        order_producer(queue, num_orders, num_workers),
        order_worker("A", queue),
        order_worker("B", queue),
        order_worker("C", queue),
    )

    print("Все заказы обработаны")

asyncio.run(main())
