from django.views.generic import TemplateView

from client.models import Client
from mailing.models import Mailing
from message.models import Message


class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Сервис рассылки писем',
        'count_mailing': Mailing.objects.all().count(),
        'count_client': Client.objects.all().count(),
        'count_message': Message.objects.all().count(),
    }

