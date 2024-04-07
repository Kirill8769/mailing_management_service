from django.contrib import admin

from .models import Attempt, Client, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'comment', )
    list_filter = ('email', )
    search_fields = ('name', 'comment', )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'periodicity', 'mailing_status', )
    list_filter = ('periodicity', 'mailing_status', 'date_first_send', )
    search_fields = ('client', 'message', )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'client', 'attempt_status', )
    list_filter = ('attempt_status', 'mailing', 'client', 'date_last_send', )
    search_fields = ('message', )
