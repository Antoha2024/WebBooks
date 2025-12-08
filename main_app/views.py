# main_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import csv
import os

def index(request):
    return render(request, 'main_app/index.html')

def translator(request):
    if request.method == 'POST':
        term = request.POST.get('search_term')
        start_url = "https://ruscorpora.ru/"
        search_data = {
            'q': term,
            'mode': 'basic',
            'lang': 'en'
        }

        session = requests.Session()
        initial_response = session.get(start_url)

        if initial_response.status_code != 200:
            return JsonResponse({'error': f"Ошибка при подключении к начальной странице: статус-код {initial_response.status_code}"})

        search_response = session.post(start_url, data=search_data)

        if search_response.status_code != 200:
            return JsonResponse({'error': f"Ошибка при поиске: статус-код {search_response.status_code}"})

        soup = BeautifulSoup(search_response.content, 'html.parser')
        results = []

        # Теперь ищем теги span с классом 'hit word'
        for hit_span in soup.find_all('span', class_='hit word'):
            # Берём ближайшего родителя (родительский div или p), содержащий предложение
            parent_element = hit_span.find_parent(['div', 'p'])
            if parent_element:
                sentence = parent_element.text.strip()
                results.append(sentence)

        # Промежуточный лог
        print(f"Results count: {len(results)}, first item: {results[:3]}")

        # Если результатов нет, возвращаем ошибку
        if len(results) == 0:
            return JsonResponse({'error': 'No results found!'})

        # Сохраняем результаты в CSV-файл
        output_path = 'examples_dataset.csv'
        with open(output_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in results:
                writer.writerow([term, row])

        return JsonResponse({'message': f'Результаты сохранены в "{output_path}".'})

    return render(request, 'index.html')