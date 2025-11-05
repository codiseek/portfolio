from django.core.management.base import BaseCommand
from main.models import Project
from django.utils import timezone

class Command(BaseCommand):
    help = 'Обновляет статистику GitHub для всех проектов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительное обновление, игнорируя временные ограничения',
        )

    def handle(self, *args, **options):
        projects = Project.objects.filter(is_published=True, github_url__isnull=False)
        updated_count = 0
        
        for project in projects:
            if project.update_github_stats(force=options['force']):
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Обновлен: {project.title} - ⭐{project.stars} 🍴{project.forks}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Успешно обновлено {updated_count} из {projects.count()} проектов')
        )