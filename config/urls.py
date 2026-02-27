"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main_app.views import home, animation_view, voice_view, speak

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Главная страница с кнопками
    path('animation/', animation_view, name='animation'),  # Страница анимации/галереи
    path('voice/', voice_view, name='voice'),  # Страница озвучки
    path('speak/', speak, name='speak'),  # AJAX обработчик для озвучки
]

# Добавляем обработку медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)