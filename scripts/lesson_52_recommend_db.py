from dataclasses import dataclass


@dataclass
class Workload:
    name: str
    structured: bool       # данные имеют чёткую фиксированную структуру
    needs_acid: bool       # нужны ACID-транзакции
    temporary: bool        # данные временные (живут по TTL)
    flexible_schema: bool  # структура документов меняется от записи к записи


def recommend_db(w: Workload) -> str:
    # Порядок проверок важен: сначала самые строгие требования.
    if w.needs_acid or (w.structured and not w.temporary and not w.flexible_schema):
        return "PostgreSQL"
    if w.temporary:
        return "Redis"
    if w.flexible_schema:
        return "MongoDB"
    return "PostgreSQL"


def main():
    workloads = [
        Workload("orders", structured=True, needs_acid=True, temporary=False, flexible_schema=False),
        Workload("products_cache", structured=False, needs_acid=False, temporary=True, flexible_schema=False),
        Workload("app_logs", structured=False, needs_acid=False, temporary=False, flexible_schema=True),
        Workload("users", structured=True, needs_acid=False, temporary=False, flexible_schema=False),
        Workload("sessions", structured=False, needs_acid=False, temporary=True, flexible_schema=False),
    ]

    counts = {"PostgreSQL": 0, "Redis": 0, "MongoDB": 0}
    for w in workloads:
        db = recommend_db(w)
        counts[db] += 1
        print(f"{w.name} -> {db}")

    print("---")
    for db in ("PostgreSQL", "Redis", "MongoDB"):
        print(f"{db}: {counts[db]}")


if __name__ == "__main__":
    main()
