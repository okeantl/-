class DocumentCollection:
    """Упрощённый аналог коллекции MongoDB: документы с гибкой схемой."""

    def __init__(self):
        self._documents = []
        self._next_id = 1

    def insert_one(self, document):
        """Вставка документа. Возвращает присвоенный _id."""
        doc = dict(document)
        doc["_id"] = self._next_id
        self._next_id += 1
        self._documents.append(doc)
        return doc["_id"]

    def _matches(self, doc, filter_query):
        for field, condition in filter_query.items():
            if isinstance(condition, dict):
                for op, value in condition.items():
                    actual = doc.get(field)
                    if actual is None:
                        return False
                    if op == "$gte" and not actual >= value:
                        return False
                    if op == "$lt" and not actual < value:
                        return False
                    if op == "$in" and actual not in value:
                        return False
            else:
                if doc.get(field) != condition:
                    return False
        return True

    def find(self, filter_query=None):
        """Поиск документов по фильтру (поддержка $gte, $lt, $in)."""
        if filter_query is None:
            filter_query = {}
        return [doc for doc in self._documents if self._matches(doc, filter_query)]

    def count_by(self, field):
        """Группировка по полю: сколько документов на каждое значение."""
        counts = {}
        for doc in self._documents:
            key = doc.get(field)
            counts[key] = counts.get(key, 0) + 1
        return counts


logs = DocumentCollection()

logs.insert_one({"type": "error", "message": "Сбой оплаты заказа", "status_code": 500})
logs.insert_one({"type": "access", "endpoint": "/api/products", "status_code": 200})
logs.insert_one({"type": "access", "endpoint": "/api/cart", "status_code": 404})
logs.insert_one({"type": "error", "message": "Товар не найден", "status_code": 404})
logs.insert_one({"type": "access", "endpoint": "/api/orders", "status_code": 503})

errors = logs.find({"type": "error"})
print(f"Логов ошибок: {len(errors)}")

failed = logs.find({"status_code": {"$gte": 400}})
print(f"Запросов с кодом >= 400: {len(failed)}")

server_side = logs.find({"status_code": {"$in": [500, 503]}})
print(f"Серверных сбоев: {len(server_side)}")

by_type = logs.count_by("type")
for log_type in sorted(by_type):
    print(f"{log_type}: {by_type[log_type]}")
