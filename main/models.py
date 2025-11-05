from django.db import models
from django.utils import timezone
import requests
from datetime import timedelta

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание')
    technologies = models.CharField(max_length=300, verbose_name='Технологии (через запятую)')
    main_image = models.ImageField(upload_to='projects/main/', verbose_name='Главное изображение', blank=True, null=True)
    github_url = models.URLField(verbose_name='GitHub ссылка', blank=True)
    github_api_url = models.CharField(max_length=500, blank=True, verbose_name='GitHub API URL')
    live_url = models.URLField(verbose_name='Live демо', blank=True)
    download_url = models.URLField(verbose_name='Ссылка для скачивания', blank=True)
    stars = models.IntegerField(default=0, verbose_name='Звезды')
    forks = models.IntegerField(default=0, verbose_name='Форки')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    last_github_sync = models.DateTimeField(null=True, blank=True, verbose_name='Последняя синхронизация с GitHub')
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        """Возвращает список технологий"""
        return [tech.strip() for tech in self.technologies.split(',')]
    
    def extract_github_info(self):
        """Извлекает владельца и название репозитория из GitHub URL"""
        if not self.github_url:
            return None, None
        
        parts = self.github_url.rstrip('/').split('/')
        if len(parts) >= 2:
            owner = parts[-2]
            repo = parts[-1]
            return owner, repo
        return None, None
    
    def get_github_api_url(self):
        """Генерирует URL для GitHub API"""
        owner, repo = self.extract_github_info()
        if owner and repo:
            return f"https://api.github.com/repos/{owner}/{repo}"
        return None
    
    def update_github_stats(self, force=False):
        """Обновляет статистику из GitHub API"""
        if not force and self.last_github_sync:
            time_since_sync = timezone.now() - self.last_github_sync
            if time_since_sync < timedelta(hours=1):
                return False
        
        api_url = self.get_github_api_url()
        if not api_url:
            return False
        
        try:
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Django-Portfolio-App'
            }
            
            response = requests.get(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.stars = data.get('stargazers_count', 0)
                self.forks = data.get('forks_count', 0)
                self.github_api_url = api_url
                self.last_github_sync = timezone.now()
                self.save()
                return True
            else:
                print(f"GitHub API error: {response.status_code} for {api_url}")
                return False
                
        except requests.RequestException as e:
            print(f"Error fetching GitHub stats: {e}")
            return False
    
    def save(self, *args, **kwargs):
        if self.github_url and not self.github_api_url:
            self.github_api_url = self.get_github_api_url()
        super().save(*args, **kwargs)

class Screenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots', verbose_name='Проект')
    image = models.ImageField(upload_to='projects/screenshots/', verbose_name='Скриншот')
    title = models.CharField(max_length=200, blank=True, verbose_name='Название скриншота')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.project.title} - {self.title or f'Скриншот {self.id}'}"