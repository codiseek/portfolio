from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'stars', 'forks', 'is_published', 'created_date')
    list_filter = ('is_published', 'created_date')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('is_published', 'stars', 'forks')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'technologies', 'image')
        }),
        ('Ссылки', {
            'fields': ('github_url', 'live_url', 'download_url')
        }),
        ('Статистика', {
            'fields': ('stars', 'forks')
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_date', 'updated_date')
        }),
    )