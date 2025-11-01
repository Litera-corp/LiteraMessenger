FROM python:3.14-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем приложение с помощью uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]