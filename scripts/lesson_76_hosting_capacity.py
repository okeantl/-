from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class Endpoint:
    name: str            # имя эндпоинта SFMShop
    expected_rps: float  # ожидаемая нагрузка, запросов/сек
    avg_ms: float        # средняя длительность одного запроса, мс


# Один воркер обрабатывает запросы последовательно: его пропускная
# способность = 1000 / avg_ms запросов в секунду.
def worker_capacity(avg_ms: float) -> float:
    return 1000.0 / avg_ms


# Сколько воркеров нужно эндпоинту, чтобы выдержать нагрузку с запасом.
def workers_needed(ep: Endpoint, headroom: float) -> int:
    target = ep.expected_rps * headroom
    return ceil(target / worker_capacity(ep.avg_ms))


# Выбор тарифа хостинга по суммарному RPS: пороги из урока.
def tier(total_rps: float) -> str:
    if total_rps < 100:
        return "VPS/PaaS"
    if total_rps <= 1000:
        return "Cloud"
    return "Cloud+K8s"


def plan(endpoints, headroom=1.5):
    rows = []
    total_rps = 0.0
    total_workers = 0
    for ep in sorted(endpoints, key=lambda e: e.name):
        w = workers_needed(ep, headroom)
        total_rps += ep.expected_rps
        total_workers += w
        rows.append((ep.name, ep.expected_rps, w))
    return rows, total_rps, total_workers


def main():
    endpoints = [
        Endpoint("catalog", 60.0, 40.0),
        Endpoint("cart", 25.0, 80.0),
        Endpoint("checkout", 8.0, 250.0),
        Endpoint("search", 35.0, 120.0),
    ]

    rows, total_rps, total_workers = plan(endpoints, headroom=1.5)

    print("Эндпоинт      RPS  Воркеры")
    for name, rps, w in rows:
        print(f"{name:<12}{rps:5.0f}  {w:>5}")
    print(f"Итого RPS: {total_rps:.0f}")
    print(f"Воркеров всего: {total_workers}")
    print(f"Тариф хостинга: {tier(total_rps)}")


if __name__ == "__main__":
    main()
