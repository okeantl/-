import pika
import json


def process_message(ch, method, properties, body):
    """Обработка сообщения"""
    message = json.loads(body)
    print(f"Получено сообщение: {message}")

    # Обработка сообщения
    # ...

    # Подтверждение обработки
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer(queue_name: str):
    """Запуск consumer"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
        )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=process_message
        )

    print(f"Ожидание сообщений в очереди {queue_name}...")
    channel.start_consuming()

# Тест consumer — запускать в другом терминале:
#   python src/services/queue_consumer.py
# start_consuming() блокирует поток, поэтому consumer и producer
# запускаются как отдельные процессы, а не в одном __main__.
if __name__ == "__main__":
    start_consumer('test_queue')
