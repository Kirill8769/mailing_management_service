from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {'title': 'Главная страница'}
