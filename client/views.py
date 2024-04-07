from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView

from .models import Client


class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Главная'}


class ClientDetailView(DetailView):
    model = Client
    extra_context = {'title': 'Детали клиента'}


class ClientCreateView(CreateView):
    model = Client
    fields = ('name', 'email', 'comment',)
    extra_context = {'title': 'Создание клиента'}
    success_url = reverse_lazy('client:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'email', 'comment',)
    extra_context = {'title': 'Обновление клиента'}

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.object.pk])


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('client:client_list')
