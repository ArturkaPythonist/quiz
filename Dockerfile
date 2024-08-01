# Используем официальный образ Python
FROM python:3.12.4

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории в контейнере
WORKDIR /app

# Установка зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальную часть кода приложения
COPY . /app/

# Запуск команды collectstatic для сборки статических файлов
RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для внешнего мира
EXPOSE 8000

# Запуск команды миграций и Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn djangoProject.wsgi:application --bind 0.0.0.0:8000"]
