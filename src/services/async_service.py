import asyncio
import aiohttp

async def fetch_url_async(url: str):
    """Асинхронный запрос к URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None

# Тест
async def main():
    url = "https://api.example.com/data"
    result = await fetch_url_async(url)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
