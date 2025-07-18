FROM python:3.13.4

WORKDIR /app

COPY . .

# Устанавливаем зависимости
RUN pip install  -r requirements.txt

# Копируем остальной код ПОСЛЕ установки зависимостей


# Исправленная команда запуска (без лишнего флага)
CMD ["python", "main.py"]