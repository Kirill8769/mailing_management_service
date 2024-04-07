from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'comment', )
    list_filter = ('email', )
    search_fields = ('name', 'comment', )
