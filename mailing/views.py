from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView

from .models import Mailing


class MailingListView(ListView):
    model = Mailing
    extra_context = {'title': 'Все рассылки'}


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {'title': 'Детали рассылки'}


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('title', 'start_date', 'periodicity', 'mailing_status', 'client', 'message',)
    extra_context = {'title': 'Создание рассылки'}
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('title', 'start_date', 'periodicity', 'mailing_status', 'client', 'message',)
    extra_context = {'title': 'Обновление рассылки'}

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.object.pk])


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {'title': 'Удаление рассылки'}
    success_url = reverse_lazy('mailing:mailing_list')


