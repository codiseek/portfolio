from django.shortcuts import render
from django.conf import settings
from .models import Project

def index(request):
    projects = Project.objects.filter(is_published=True)
    
    projects_data = []
    for project in projects:
        # Правильное формирование URL изображения
        if project.image:
            image_url = project.image.url
        else:
            image_url = '/static/images/project-default.jpg'
        
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'technologies': project.get_technologies_list(),
            'image_url': image_url,
            'github_url': project.github_url,
            'live_url': project.live_url,
            'download_url': project.download_url,
            'stars': project.stars,
            'forks': project.forks,
            # Убрали language и language_color
        })
    
    context = {
        'projects': projects_data
    }
    return render(request, 'main/index.html', context)