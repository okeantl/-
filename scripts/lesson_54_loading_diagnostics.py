def diagnose_loading(stages):
    total = sum(stages.values())
    bottleneck = max(stages, key=lambda name: stages[name])
    return total, bottleneck


STAGE_NAMES = {
    "dns": "DNS-запрос",
    "tcp": "TCP-подключение",
    "server": "Обработка на сервере",
    "transfer": "Передача данных",
    "render": "Рендеринг на клиенте",
}


def report(stages):
    total, bottleneck = diagnose_loading(stages)
    print(f"Общее время загрузки: {total:.2f} сек")
    for name in ("dns", "tcp", "server", "transfer", "render"):
        ms = stages[name]
        percent = ms / total * 100
        print(f"{STAGE_NAMES[name]}: {ms:.2f} сек ({percent:.1f}%)")
    print(f"Узкое место: {STAGE_NAMES[bottleneck]}")


measurements = {
    "dns": 0.05,
    "tcp": 0.20,
    "server": 2.50,
    "transfer": 0.80,
    "render": 0.45,
}

report(measurements)
