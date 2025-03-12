# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Открываем порт, который будет использовать Streamlit
EXPOSE 8501

# Команда для запуска Streamlit-приложения
CMD ["streamlit", "run", "src/app.py", "--server.port=80", "--server.address=0.0.0.0"]