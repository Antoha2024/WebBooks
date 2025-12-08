from transformers import BertModel, BertTokenizerFast
import torch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Загрузка и настройка transformer-модели
model_name = "DeepPavlov/rubert-base-cased-conversational"
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Фунция для выбора ключевых слов
def extract_keywords(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)

    # Берём первые 10 важнейших слов (упрощённая реализация)
    top_n = 10
    most_important_words = sorted(inputs.input_ids.squeeze().tolist(), reverse=True)[:top_n]
    decoded_words = tokenizer.convert_ids_to_tokens(most_important_words)
    return decoded_words

# Часть для автоматического взаимодействия с сайтом
def search_on_ruscorpora(keywords):
    # Установка драйвера chrome
    driver_path = ChromeDriverManager().install()
    service = Service(executable_path=driver_path)

    with webdriver.Chrome(service=service) as driver:
        # Переходим на главную страницу сайта
        driver.get('https://ruscorpora.ru/search')
        
        # Ожидаем появление формы поиска
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "the-input__input")))
        
        # Проходим через каждое ключевое слово
        results = {}
        for keyword in keywords:
            # Вводим ключевое слово в форму поиска
            input_field.clear()
            input_field.send_keys(keyword)
            
            # Находим кнопку поиска и нажимаем её
            buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".button--color-colored.medium.button--mode-default.button")))
            first_search_button = buttons[0]
            first_search_button.click()
            
            # Дождёмся полного рендеринга страницы
            time.sleep(5)
            
            # Парсим первый найденный абзац с результатом
            highlighted_words = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hit.word i')))
            if len(highlighted_words) > 0:
                first_highlighted_word = highlighted_words[0]
                parent_paragraph = first_highlighted_word.find_element(By.XPATH, "./ancestor::p")
                paragraph_text = parent_paragraph.text
                
                # Сохраняем результат для текущего ключевого слова
                results[keyword] = paragraph_text
        
        return results

# Основной поток выполнения
if __name__ == "__main__":
    input_text = input("Введите текст: ")
    keywords = extract_keywords(input_text)
    print(f"\nВыделенные ключевые слова: {keywords}\n")

    # Поиск каждой ключевой фразы на сайте
    search_results = search_on_ruscorpora(keywords)

    # Печать результатов поиска
    for keyword, result in search_results.items():
        print(f'\nПо запросу "{keyword}" найдены переводы:')
        print(result)
        print('-'*50)