# Використовуйте офіційний образ Python
FROM python:3.12-slim

# Встановлюємо та встановлюємо залежності
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли з поточної директорії в /app контейнера
COPY 12_Auth_and_Auth /app

# Запускаємо проект
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
