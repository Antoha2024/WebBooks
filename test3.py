from transformers import BertModel, BertTokenizerFast
import torch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Загрузка и настройка трансформер-модели
model_name = "DeepPavlov/rubert-base-cased-conversational"
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Функция для выбора ключевых слов
def extract_keywords(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)

    # Преобразуем токены обратно в слова и получаем топ-N значимых слов
    tokens = tokenizer.tokenize(text)
    token_embeddings = outputs.last_hidden_state[0].detach().cpu().numpy()
    importance_scores = [(i, score) for i, score in enumerate(token_embeddings.sum(axis=-1))]
    important_indices = sorted(importance_scores, key=lambda x: x[1], reverse=True)[:10]
    important_words = [tokens[i] for i, _ in important_indices]
    return important_words

# Часть для автоматического взаимодействия с сайтом
def search_on_ruscorpora(keywords):
    # Установка драйвера Chrome
    driver_path = ChromeDriverManager().install()
    service = Service(executable_path=driver_path)

    with webdriver.Chrome(service=service) as driver:
        # Переходим на главную страницу сайта
        driver.get('https://ruscorpora.ru/')
        
        # Ожидаем появление формы поиска
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(EC.visibility_of_element_located((By.ID, "q")))
        
        # Проходим через каждое ключевое слово
        results = {}
        for keyword in keywords:
            # Вводим ключевое слово в форму поиска
            input_field.clear()
            input_field.send_keys(keyword)
            
            # Находим кнопку поиска и нажимаем её
            search_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
            search_button.click()
            
            # Дожидаемся отображения результатов
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "hit")))
            
            # Находим выделенные слова и контекст вокруг них
            highlighted_words = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hit.word i')))
            if len(highlighted_words) > 0:
                first_highlighted_word = highlighted_words[0]
                parent_element = first_highlighted_word.find_element(By.XPATH, "./ancestor::*[@class='example']")
                context = parent_element.text
                
                # Сохраняем результат для текущего ключевого слова
                results[keyword] = context
        
        return results

# Основной поток выполнения
if __name__ == "__main__":
    input_text = "Программирование на Python становится всё популярнее."
    keywords = extract_keywords(input_text)
    print(f"\nВыделенные ключевые слова: {keywords}\n")

    # Поиск каждой ключевой фразы на сайте
    search_results = search_on_ruscorpora(keywords)

    # Печать результатов поиска
    for keyword, result in search_results.items():
        print(f'\nПо запросу "{keyword}" найдены переводы:')
        print(result)
        print('-'*50)