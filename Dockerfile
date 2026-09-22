FROM python:3.14-slim

# Устанавливаем uv внутрь контейнера
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Копируем ТОЛЬКО файлы зависимостей первым слоем (для кеширования)
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости без dev-группы
RUN uv sync --frozen --no-dev

# Копируем остальной код проекта
COPY . .

# Команда запуска бота
CMD ["uv", "run", "python", "run.py"]