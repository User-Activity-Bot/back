FROM python:3.12

# Устанавливаем переменную среды для запуска в режиме неинтерактивного режима
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY telegram_activity/ /app/

# Определяем порт, который будет слушать приложение
EXPOSE 8000

# Запускаем команду для запуска сервера Django
CMD python manage.py makemigrations  && \
    python manage.py migrate  && \
    python manage.py collectstatic && \
    python manage.py runserver 0.0.0.0:8000
    #gunicorn --bind 0.0.0.0:8000 cosmomoll_back.wsgi
