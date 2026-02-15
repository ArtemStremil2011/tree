from django.contrib import admin
from .models import Person, PersonFile

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'info_preview', 'user', 'parent', 'level')
    list_filter = ('user', 'level')
    search_fields = ('name', 'info')
    
    def info_preview(self, obj):
        return obj.info[:50] + '...' if obj.info and len(obj.info) > 50 else obj.info
    info_preview.short_description = 'Информация'

@admin.register(PersonFile)
class PersonFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'file', 'uploaded_at')
    list_filter = ('person__user',)  # фильтр по владельцу