import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Автоподбор и установка подходящей версии chromedriver
driver_path = ChromeDriverManager().install()

# Настройка браузера в обычном режиме (без headless)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Закомментирована данная строка

# Запуск браузера
with webdriver.Chrome(service=Service(driver_path), options=options) as driver:
    # Открываем страницу поиска
    driver.get('https://ruscorpora.ru/search?search=CgkyBwgFEgNiZWw%253D')

    # Закрываем cookie-баннер, если он мешает (элемент с классом "cookie-info-box")
    try:
        close_cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookie-info-box button"))
        )
        close_cookie_button.click()
    except Exception as e:
        pass  # Игнорируем, если баннера нет

    # Ждем появления поля ввода (используем классы)
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".the-input__input"))
    )

    # Вводим слово "здоровье"
    input_field.clear()
    input_field.send_keys('здоровье')

    # Ждем появления кнопки "Искать" (используем классы)
    search_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".button--color-colored.medium.button--mode-default.button"))
    )
    # Первая кнопка (идентичных кнопок много, выбираем первую)
    first_search_button = search_buttons[0]

    # Нажимаем кнопку поиска, предварительно проверив доступность
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(first_search_button)).click()

    # Ждем полной загрузки страницы и появления результатов
    WebDriverWait(driver, 15).until(
        lambda drv: drv.execute_script("return document.readyState === 'complete'")
    )

    # Дополнительное ожидание полной динамики страницы
    time.sleep(10)  # Задержка для большей уверенности

    # Получаем URL текущей страницы (URL не изменится!)
    current_url = driver.current_url
    print(f"Текущий URL страницы с результатами: {current_url}")

    # Используя более надежный и простой CSS-селектор
    try:
    # Находим первое слово с выделением
        first_highlighted_word = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.hit.word i'))
        )
        print(f"Первое выделенное слово: {first_highlighted_word.text.strip()}")

    # Находим родительский элемент, содержащий весь абзац (например, ближайший <p> или другой контейнер)
        paragraph_element = first_highlighted_word.find_element(By.XPATH, './ancestor::p')
        paragraph_text = paragraph_element.text
        print(f"Весь абзац:\n{paragraph_text}")

        first_highlighted_word = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.word i'))
        )
        print(f"Первое выделенное слово: {first_highlighted_word.text.strip()}")

    # Находим родительский элемент, содержащий весь абзац (например, ближайший <p> или другой контейнер)
        paragraph_element = first_highlighted_word.find_element(By.XPATH, './ancestor::p')
        paragraph_text = paragraph_element.text
        print(f"Весь абзац:\n{paragraph_text}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Браузер закрыт после выполнения операции