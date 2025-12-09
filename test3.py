from transformers import BertModel, BertTokenizerFast
import torch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Загружаем и настраиваем трансформер-модель
model_name = "DeepPavlov/rubert-base-cased-conversational"
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Функция для выбора ключевых слов
def extract_keywords(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)

    # Простая сортировка первых 10 важных слов
    top_n = 10
    most_important_words = sorted(inputs.input_ids.squeeze().tolist(), reverse=True)[:top_n]
    decoded_words = tokenizer.convert_ids_to_tokens(most_important_words)
    return decoded_words

# Функция для взаимодействия с сайтом
def search_on_ruscorpora(keywords):
    # Установка драйвера Chrome
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)

    # Запускаем Chrome в headless-режиме
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        # Переходим на главную страницу
        driver.get('https://ruscorpora.ru/')
        
        # Ожидание загрузки формы поиска
        wait = WebDriverWait(driver, 20)
        input_field = wait.until(EC.visibility_of_element_located((By.ID, "q")))
        
        # Список результатов
        results = {}
        for keyword in keywords:
            # Вводим ключевое слово
            input_field.clear()
            input_field.send_keys(keyword)
            
            # Нажимаем кнопку поиска
            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
            submit_button.click()
            
            # Ожидаем появления результатов
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "hit")))
            
            # Находим первый выделенный фрагмент
            highlighted_words = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hit.word i')))
            if len(highlighted_words) > 0:
                first_highlighted_word = highlighted_words[0]
                parent_element = first_highlighted_word.find_element(By.XPATH, "./ancestor::*[@class='example']")
                paragraph_text = parent_element.text
                results[keyword] = paragraph_text
        
        return results

# Основной поток выполнения
if __name__ == "__main__":
    input_text = "Пример текста"
    keywords = extract_keywords(input_text)
    print(f"\nВыделенные ключевые слова: {keywords}\n")

    # Проводим поиск на сайте ruscorpora
    search_results = search_on_ruscorpora(keywords)

    # Выводим результаты поиска
    for keyword, result in search_results.items():
        print(f'\nПо запросу "{keyword}" найдены переводы:')
        print(result)
        print('-'*50)