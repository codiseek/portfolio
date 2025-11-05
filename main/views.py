from django.shortcuts import render
from django.conf import settings
from .models import Project

def index(request):
    projects = Project.objects.filter(is_published=True).prefetch_related('screenshots')
    
    # Автоматически обновляем статистику для проектов, которые давно не обновлялись
    for project in projects:
        if project.github_url:
            project.update_github_stats()
    
    projects_data = []
    for project in projects:
        # Главное изображение
        if project.main_image:
            main_image_url = project.main_image.url
        else:
            main_image_url = None
        
        # Собираем скриншоты
        screenshots_data = []
        for screenshot in project.screenshots.all():
            screenshots_data.append({
                'id': screenshot.id,
                'image_url': screenshot.image.url,
                'title': screenshot.title,
                'order': screenshot.order,
            })
        
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'technologies': project.get_technologies_list(),
            'main_image_url': main_image_url,
            'screenshots': screenshots_data,
            'github_url': project.github_url,
            'live_url': project.live_url,
            'download_url': project.download_url,
            'stars': project.stars,
            'forks': project.forks,
        })
    
    context = {
        'projects': projects_data
    }
    return render(request, 'main/index.html', context)