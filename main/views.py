from django.views.generic import TemplateView

from blog.models import Blog
from client.models import Client
from mailing.models import Mailing
from message.models import Message


from django.db.models import Count


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сервис рассылки писем'
        context['dict_info'] = {
            'Количество рассылок': Mailing.objects.all().count(),
            'Количество активных рассылок': Mailing.objects.filter(mailing_status='R').count(),
            'Количество уникальных клиентов': Client.objects.values('email').annotate(total=Count('email')).count(),
        }
        blogs = list(Blog.objects.all().order_by('?'))
        while len(blogs) < 3:
            blogs.append({'title': 'Место для заголовка блога', 'content': 'Место для описания блога'})
        context['blogs'] = blogs[:3]

        return context
