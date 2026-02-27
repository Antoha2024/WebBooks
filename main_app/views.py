from django.shortcuts import render, redirect
from django.http import JsonResponse
from gtts import gTTS
import uuid
import os
from django.conf import settings

def home(request):
    """Новая главная страница с кнопками Анимация и Озвучка"""
    return render(request, 'main_app/home.html')

def animation_view(request):
    """Страница с галереей изображений (Drag & Drop интерфейс)"""
    return render(request, 'main_app/animation.html')

def voice_view(request):
    """Страница с формой для озвучки текста"""
    return render(request, 'main_app/voice.html')

def speak(request):
    """Обработчик AJAX запросов для озвучки текста"""
    if request.method == 'POST':
        text = request.POST.get('search_term')
        
        if not text or text.strip() == '':
            return JsonResponse({'error': 'Введите текст для озвучивания'}, status=400)
        
        # Создаем директорию media, если она не существует
        media_dir = settings.MEDIA_ROOT
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
            print(f"Создана директория: {media_dir}")
        
        try:
            tts = gTTS(text=text, lang='ru')
            
            # Уникальное имя файла
            filename = f'speech_{uuid.uuid4().hex}.mp3'
            filepath = os.path.join(media_dir, filename)
            
            # Сохраняем файл в MEDIA_ROOT
            tts.save(filepath)
            
            # Формируем URL к файлу
            audio_url = f'{settings.MEDIA_URL}{filename}'
            
            # Ответ с информацией о файле
            response_data = {
                'audio_url': audio_url,
                'message': 'Текст успешно озвучен',
                'filename': filename
            }
            return JsonResponse(response_data)
        
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return JsonResponse({'error': f'Ошибка при создании аудиофайла: {str(e)}'}, status=500)
    
    else:
        return redirect('home')