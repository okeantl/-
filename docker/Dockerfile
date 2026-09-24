# Этап 1: builder - устанавливаем зависимости
FROM python:3.11-slim as builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Этап 2: финальный образ
FROM python:3.11-slim
WORKDIR /app

# Копируем только установленные пакеты из builder
COPY --from=builder /root/.local /root/.local

# Копируем код приложения
COPY . .

# Добавляем пользовательские пакеты в PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
