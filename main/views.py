from django.views.generic import TemplateView

from client.models import Client
from mailing.models import Mailing
from message.models import Message


class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Сервис рассылки писем',
        'dict_info': {
            'Количество рассылок': Mailing.objects.all().count(),
            'Количество клиентов': Client.objects.all().count(),
            'Количество сообщений': Message.objects.all().count(),
        },
    }

