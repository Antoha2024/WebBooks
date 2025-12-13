# Использование базы с конкретной версией PyTorch и CUDA
FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-runtime

# Обновляем пакеты и устанавливаем браузерные компоненты
RUN apt-get update && \
    apt-get install -y chromium-chromedriver wget unzip xvfb fonts-noto-color-emoji libgconf-2-4

# Ставим нужные Python-библиотеки
RUN pip install selenium webdriver-manager requests transformers django beautifulsoup4

# Скопируем скрипт внутрь контейнера
COPY test3.py .

# Команда запуска скрипта
CMD ["python", "test3.py"]