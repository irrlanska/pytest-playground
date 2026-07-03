# Базовый образ — лёгкая версия Python 3.12
FROM python:3.12-slim

# Создаём рабочую папку внутри контейнера
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (тесты, conftest, pytest.ini)
COPY . .

# Точка входа — pytest, аргументы — через CMD
ENTRYPOINT ["pytest"]
CMD ["-v"]