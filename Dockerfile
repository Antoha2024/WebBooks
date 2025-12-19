# Используем образ от PyTorch как самую стабильную базу для ИИ
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Устанавливаем системные зависимости для работы с текстом
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Ставим обе ваши библиотеки
RUN pip install --no-cache-dir transformers==4.30.0 pymorphy3

# Скачиваем русскую модель заранее
RUN python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')"

# Скачиваем русскую модель заранее
RUN python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')"

# Копируем файл test3.py в контейнер
COPY test3.py /app/

WORKDIR /app
