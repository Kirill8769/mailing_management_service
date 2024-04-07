from django.contrib import admin

from .models import Attempt, Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'start_date', 'end_date', 'periodicity', 'mailing_status', )
    list_filter = ('periodicity', 'mailing_status', 'start_date', 'end_date', )
    search_fields = ('title', 'client', 'message', )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'client', 'attempt_status', )
    list_filter = ('attempt_status', 'mailing', 'client', 'date_send', )
    search_fields = ('message', 'answer_server', )
