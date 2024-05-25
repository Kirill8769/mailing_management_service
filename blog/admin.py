from django.contrib import admin

from .models import Blog


@admin.register(Blog)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'publication_date', 'views_count', )
    search_fields = ('title', 'content', 'publication_date', )
