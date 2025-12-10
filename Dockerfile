FROM pytorch/pytorch:2.6.0-cuda11.7-cudnn8-runtime

# Обновляем пакеты и устанавливаем Chromium и драйвер Chrome
RUN apt-get update && \
    apt-get install -y chromium-chromedriver wget unzip xvfb fonts-noto-color-emoji libgconf-2-4

# Устанавливаем необходимые Python-пакеты
RUN pip install selenium webdriver-manager requests transformers django beautifulsoup4

# Копируем ваш скрипт внутрь контейнера
COPY test3.py .

# Запускаем скрипт
CMD ["python", "test3.py"]