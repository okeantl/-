from queue import Queue


class MessageBroker:
    """Простой брокер сообщений в памяти для проекта SFMShop.

    Producer кладёт задачи в очередь, Consumer забирает их и обрабатывает.
    При ошибке задача повторяется до max_retries раз, после чего уходит
    в очередь ошибок (dead-letter queue).
    """

    def __init__(self, max_retries=3):
        self.queue = Queue()
        self.dead_letter = []
        self.max_retries = max_retries

    def publish(self, task):
        """Producer: положить задачу в очередь."""
        self.queue.put(task)

    def consume(self, handlers):
        """Consumer: обработать все задачи из очереди.

        handlers - словарь {имя_задачи: функция}. Функция возвращает True
        при успехе и False при ошибке. При ошибке задача повторяется,
        пока число попыток не превысит max_retries.
        """
        while not self.queue.empty():
            task = self.queue.get()
            name = task["task"]
            handler = handlers[name]
            ok = handler(task)
            if ok:
                print(f"OK {name} order={task['order_id']} attempt={task['attempts'] + 1}")
            else:
                task["attempts"] += 1
                if task["attempts"] < self.max_retries:
                    print(f"RETRY {name} order={task['order_id']} attempt={task['attempts']}")
                    self.queue.put(task)
                else:
                    print(f"DEAD {name} order={task['order_id']} attempts={task['attempts']}")
                    self.dead_letter.append(task)
            self.queue.task_done()


# Обработчики задач SFMShop.
# update_stock падает первые две попытки, затем проходит.
def handle_send_email(task):
    return True


def handle_update_stock(task):
    return task["attempts"] >= 2


def handle_generate_report(task):
    return False  # Всегда падает -> уйдёт в dead-letter.


def main():
    broker = MessageBroker(max_retries=3)
    broker.publish({"task": "send_email", "order_id": 101, "attempts": 0})
    broker.publish({"task": "update_stock", "order_id": 101, "attempts": 0})
    broker.publish({"task": "generate_report", "order_id": 101, "attempts": 0})

    handlers = {
        "send_email": handle_send_email,
        "update_stock": handle_update_stock,
        "generate_report": handle_generate_report,
    }
    broker.consume(handlers)

    print(f"Dead-letter: {len(broker.dead_letter)}")
    for task in broker.dead_letter:
        print(f"  {task['task']} order={task['order_id']}")


if __name__ == "__main__":
    main()
