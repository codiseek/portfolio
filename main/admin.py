from django.contrib import admin
from .models import Project, Screenshot
from django.utils import timezone
from datetime import timedelta

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 1
    fields = ('image', 'title', 'order')
    ordering = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'stars', 'forks', 'is_published', 'created_date', 'last_github_sync')
    list_filter = ('is_published', 'created_date')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('is_published', 'stars', 'forks')
    readonly_fields = ('created_date', 'updated_date', 'last_github_sync', 'github_api_url')
    actions = ['update_github_stats_action']
    inlines = [ScreenshotInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'technologies', 'main_image')
        }),
        ('Ссылки', {
            'fields': ('github_url', 'live_url', 'download_url')
        }),
        ('Статистика', {
            'fields': ('stars', 'forks', 'github_api_url', 'last_github_sync')
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_date', 'updated_date')
        }),
    )
    
    def update_github_stats_action(self, request, queryset):
        updated_count = 0
        for project in queryset:
            if project.update_github_stats(force=True):
                updated_count += 1
        
        self.message_user(
            request, 
            f"Статистика GitHub обновлена для {updated_count} из {queryset.count()} проектов"
        )
    
    update_github_stats_action.short_description = "Обновить статистику GitHub для выбранных проектов"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.github_url:
            obj.update_github_stats()

@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'order')
    list_filter = ('project',)
    search_fields = ('project__title', 'title')
    list_editable = ('order',)