from collections import deque


class TaskQueueSimulator:
    """Симулятор очереди задач с retry-логикой (как в consumer RabbitMQ).

    Задачи обрабатываются по очереди. Если обработчик задачи
    бросает исключение, задача возвращается в конец очереди
    с увеличенным счётчиком попыток (x-retry-count). После
    исчерпания max_retries задача уходит в очередь ошибок.
    """

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.queue: deque = deque()
        self.errors: list[dict] = []
        self.done: list[int] = []

    def publish(self, order_id: int) -> None:
        """Положить задачу в очередь (retry-count = 0)."""
        self.queue.append({"order_id": order_id, "retry_count": 0})

    def run(self, handler) -> None:
        """Разобрать очередь, вызывая handler(order_id) для каждой задачи."""
        while self.queue:
            task = self.queue.popleft()
            order_id = task["order_id"]
            try:
                handler(order_id)
            except Exception as exc:
                if task["retry_count"] < self.max_retries:
                    task["retry_count"] += 1
                    print(
                        f"Заказ {order_id}: ошибка ({exc}), "
                        f"повтор {task['retry_count']}/{self.max_retries}"
                    )
                    self.queue.append(task)
                else:
                    print(f"Заказ {order_id}: исчерпаны попытки, в очередь ошибок")
                    self.errors.append(task)
            else:
                self.done.append(order_id)
                print(f"Заказ {order_id}: обработан")


# Обработчик: заказ 102 всегда падает, заказ 104 падает первые 2 раза
_attempts: dict[int, int] = {}


def handle_order(order_id: int) -> None:
    _attempts[order_id] = _attempts.get(order_id, 0) + 1
    if order_id == 102:
        raise ValueError("нет товара на складе")
    if order_id == 104 and _attempts[order_id] <= 2:
        raise ValueError("таймаут платёжного шлюза")


if __name__ == "__main__":
    sim = TaskQueueSimulator(max_retries=3)
    for oid in [101, 102, 103, 104]:
        sim.publish(oid)
    sim.run(handle_order)

    print("---")
    print(f"Обработано: {sorted(sim.done)}")
    print(f"В очереди ошибок: {[t['order_id'] for t in sim.errors]}")
