# main_app/models.py
from django.db import models
import os
from django.utils import timezone

def upload_to(instance, filename):
    # Создаем путь для сохранения файла: gallery/год/месяц/день/filename
    ext = filename.split('.')[-1]
    filename = f"{instance.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('gallery', filename)

class GalleryImage(models.Model):
    """
    Модель для изображений в галерее
    """
    image = models.ImageField(upload_to=upload_to, verbose_name="Изображение")
    title = models.CharField(max_length=200, verbose_name="Название", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"
        ordering = ['order', '-upload_date']
    
    def __str__(self):
        return self.title if self.title else f"Изображение {self.id}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Присваиваем порядковый номер при создании
            last_image = GalleryImage.objects.order_by('-order').first()
            if last_image:
                self.order = last_image.order + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)

class AudioFile(models.Model):
    """
    Модель для аудиофайлов сгенерированной речи
    """
    text = models.TextField(verbose_name="Текст")
    audio_file = models.FileField(upload_to='audio/', verbose_name="Аудиофайл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Аудиофайл"
        verbose_name_plural = "Аудиофайлы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Аудио для: {self.text[:50]}..."