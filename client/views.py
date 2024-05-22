from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView

from .forms import ClientForm
from .models import Client


class ClientListView(ListView):
    """ Контроллер списка клиентов """

    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        """
        Метод возвращает список клиентов согласно правам доступа,
        если пользователь не авторизован, то возвращает пустой список.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return Client.objects.all()
            if user.has_perm('client.can_view_clients'):
                return Client.objects.all()
            return Client.objects.filter(owner=user)
        return Client.objects.none()


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер детальной информации о клиенте """

    model = Client
    extra_context = {'title': 'Детали клиента'}

    def get_object(self, queryset=None):
        """
        Метод проверяет права доступа и если права на просмотр деталей клиента есть,
        то возвращает объект клиента, иначе создаёт ошибку доступа.

        :return: Объект с информацией о клиенте.
        """
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        if user.has_perm('client.view_client'):
            return obj
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер формы создания клиента """

    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Создание клиента'}
    success_url = reverse_lazy('client:client_list')

    def get_initial(self) -> dict:
        """
        Метод инициирует пользователя и записывает его в словарь.

        :return: Словарь с информацией о пользователе.
        """
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        """
        Метод проверяет валидность заполненной формы и заносит в поле owner текущего пользователя.

        :param form: Заполненная форма
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер формы изменения клиента """

    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Обновление клиента'}
    success_url = reverse_lazy('client:client_list')

    def get_object(self, queryset=None):
        """
        Метод проверяет права доступа и если права на редактирование клиента есть,
        то возвращает объект клиента, иначе создаёт ошибку доступа

        :return: Объект с информацией о клиенте.
        """
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied

    def get_initial(self):
        """
        Метод инициирует пользователя и записывает его в словарь.

        :return: Словарь с информацией о пользователе.
        """
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер удаления клиента """

    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('client:client_list')

    def get_object(self, queryset=None):
        """
        Метод проверяет права доступа и если права на удаление клиента есть,
        то возвращает объект клиента, иначе создаёт ошибку доступа

        :return: Объект с информацией о клиенте.
        """
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied
