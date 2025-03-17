# Используем официальный образ Python
FROM python:latest

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем пакеты
RUN pip install django
RUN pip install djangorestframework
RUN pip install psycopg2
RUN pip install djoser

# Открываем порт для Django
EXPOSE 8000

# Команда для старта Django приложения
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["tail", "-f", "/dev/null"]