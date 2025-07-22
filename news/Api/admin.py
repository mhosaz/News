from django.contrib import admin
from .models import News , Tag

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    ordering = ['created']
    list_display = ['title', 'created']
admin.site.register(Tag)
