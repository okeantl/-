import re

# Учебный фрагмент requirements.txt для разбора (не файл проекта)
REQUIREMENTS = """\
fastapi==0.104.1
uvicorn==0.24.0
# веб-сервер и фреймворк выше

pytest==7.4.3
psycopg2-binary==2.9.9
redis==5.0.1
sqlalchemy>=2.0.0
pika
"""


def parse_requirements(text):
    """Разбирает строки requirements.txt в список (имя, оператор, версия)."""
    pattern = re.compile(r"^([A-Za-z0-9_-]+)\s*(==|>=|<=|~=)?\s*([0-9.]+)?$")
    result = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = pattern.match(line)
        if not match:
            continue
        name, op, version = match.groups()
        result.append((name, op, version))
    return result


def main():
    packages = parse_requirements(REQUIREMENTS)

    pinned = [name for name, op, ver in packages if op == "=="]
    unpinned = [name for name, op, ver in packages if op != "=="]

    print(f"Всего зависимостей: {len(packages)}")
    print(f"Зафиксировано (==): {len(pinned)}")
    print(f"Не зафиксировано: {len(unpinned)}")
    print("Незафиксированные пакеты:")
    for name in sorted(unpinned):
        print(f"  - {name}")


if __name__ == "__main__":
    main()
