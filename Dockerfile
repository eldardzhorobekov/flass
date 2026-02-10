# Используем ту же версию, что и локально
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Системные зависимости для сборки некоторых библиотек
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# -u (unbuffered) критически важен для Python 3.13, чтобы логи не застревали
CMD ["python", "-u", "main.py"]