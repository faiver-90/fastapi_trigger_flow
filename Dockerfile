FROM python:3.11-slim

## Установка системных зависимостей
#RUN apt-get update && apt-get install -y \
#    gcc \
#    libpq-dev \
#    python3-dev \
#    curl

## Poetry
#RUN pip install poetry
#
#ENV POETRY_NO_INTERACTION=1
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#ENV PYTHONPATH=/app
#
## Отключаем создание .venv
#RUN poetry config virtualenvs.create false

# Устанавливаем рабочую директорию
WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
#
## Копируем зависимости и устанавливаем
#COPY pyproject.toml poetry.lock* ./
#RUN poetry install --no-root
#
## Копируем остальной код в поддиректорию
#COPY . /app
