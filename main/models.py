from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание')
    technologies = models.CharField(max_length=300, verbose_name='Технологии (через запятую)')
    image = models.ImageField(upload_to='projects/', verbose_name='Изображение', blank=True, null=True)
    github_url = models.URLField(verbose_name='GitHub ссылка', blank=True)
    live_url = models.URLField(verbose_name='Live демо', blank=True)
    download_url = models.URLField(verbose_name='Ссылка для скачивания', blank=True)
    stars = models.IntegerField(default=0, verbose_name='Звезды')
    forks = models.IntegerField(default=0, verbose_name='Форки')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        """Возвращает список технологий"""
        return [tech.strip() for tech in self.technologies.split(',')]