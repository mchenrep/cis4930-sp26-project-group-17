from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "value", "created_at")
    search_fields = ("name", "category")
    list_filter = ("category",)
