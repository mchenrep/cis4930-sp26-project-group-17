from django.contrib import admin
from .models import User, Language, Repository


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'repo_count']
    search_fields = ['username']

    def repo_count(self, obj):
        return obj.repos.count()
    repo_count.short_description = 'Repositories'


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'repo_count']
    search_fields = ['name']

    def repo_count(self, obj):
        return obj.repos.count()
    repo_count.short_description = 'Repositories'


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['repo_name', 'owner', 'language', 'stars', 'source', 'fetched_at']
    search_fields = ['repo_name', 'owner__username']
    list_filter = ['source', 'language', 'fetched_at']
    autocomplete_fields = ['owner', 'language']
    list_per_page = 25