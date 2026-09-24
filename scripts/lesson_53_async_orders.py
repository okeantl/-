import asyncio


async def enrich_order(order_id: str, amount: float, delay: float) -> dict:
    """Асинхронно «обогащает» заказ: имитирует обращение к сервису."""
    await asyncio.sleep(delay)
    return {"order_id": order_id, "amount": amount, "with_vat": round(amount * 1.2, 2)}


async def process_orders(orders: list[tuple[str, float, float]]) -> list[dict]:
    """Обрабатывает все заказы параллельно и сохраняет исходный порядок."""
    tasks = [enrich_order(oid, amount, delay) for oid, amount, delay in orders]
    return await asyncio.gather(*tasks)


async def main() -> None:
    orders = [
        ("SFM-101", 1500.0, 0.03),
        ("SFM-102", 800.0, 0.01),
        ("SFM-103", 2400.0, 0.02),
    ]
    results = await process_orders(orders)
    for item in results:
        print(f"{item['order_id']}: {item['amount']} -> {item['with_vat']}")
    total = sum(item["with_vat"] for item in results)
    print(f"Итого с НДС: {round(total, 2)}")


if __name__ == "__main__":
    asyncio.run(main())
