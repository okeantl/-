# ==================== Этап 1: builder ====================
FROM python:3.11-slim AS builder

WORKDIR /app

# Ставим зависимости в отдельный слой, чтобы кэшировать
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==================== Этап 2: финальный образ ====================
FROM python:3.11-slim

# Не пишем .pyc, не буферизуем stdout (логи сразу в docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /root/.local /root/.local

# Копируем код приложения (.dockerignore исключает всё лишнее)
COPY . .

# Healthcheck: раз в 30 секунд бьём в /docs
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]