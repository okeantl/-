import asyncio


async def check_supplier(name: str, product_id: int, delay: float, price: int):
    """Имитация запроса к поставщику"""
    await asyncio.sleep(delay)
    return {"supplier": name, "product_id": product_id, "price": price}


async def check_supplier_timeout(name: str, product_id: int):
    """Поставщик, который не отвечает: через 2 секунды бросаем TimeoutError"""
    await asyncio.sleep(2.0)
    raise TimeoutError(f"Поставщик {name} не отвечает")


async def find_best_price(product_id: int) -> dict:
    """Найти лучшую цену среди поставщиков"""
    results = await asyncio.gather(
        check_supplier("Альфа", product_id, 1.0, 1500),
        check_supplier("Бета", product_id, 0.5, 1200),
        check_supplier_timeout("Гамма", product_id),
        check_supplier("Дельта", product_id, 1.5, 1350),
        return_exceptions=True
        )

    # Фильтрация успешных результатов
    valid_results = [r for r in results if not isinstance(r, Exception)]

    if not valid_results:
        return {"error": "Ни один поставщик не ответил"}

    # Поиск лучшей цены
    best = min(valid_results, key=lambda x: x["price"])
    return best


async def main():
    # Лимит 3 секунды: «Гамма» отваливается через 2 секунды, остальные успевают
    try:
        result = await asyncio.wait_for(find_best_price(42), timeout=3.0)
        print(f"Лучшая цена: {result}")
    except asyncio.TimeoutError:
        print("Превышено время ожидания")

    # Лимит 1 секунда: gather() ещё ждёт поставщиков, и wait_for() обрывает поиск
    try:
        result = await asyncio.wait_for(find_best_price(42), timeout=1.0)
        print(f"Лучшая цена: {result}")
    except asyncio.TimeoutError:
        print("Превышено время ожидания")

if __name__ == "__main__":
    asyncio.run(main())
