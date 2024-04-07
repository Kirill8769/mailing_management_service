from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView

from .models import Message


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Все письма'}


class MessageDetailView(DetailView):
    model = Message
    extra_context = {'title': 'Детали письма'}


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'body', )
    extra_context = {'title': 'Создание письма'}
    success_url = reverse_lazy('message:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body', )
    extra_context = {'title': 'Обновление письма'}

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.object.pk])


class MessageDeleteView(DeleteView):
    model = Message
    extra_context = {'title': 'Удаление письма'}
    success_url = reverse_lazy('message:message_list')
