FROM python:3.12-slim

# рабочая директория внутри контейнера
WORKDIR /app

# копируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# копируем весь проект
COPY . .

# порт FastAPI
EXPOSE 8000

# команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]