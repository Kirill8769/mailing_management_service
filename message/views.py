from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView

from .models import Message
from .services import get_messages_from_cache


class MessageListView(ListView):
    """ Контроллер списка сообщений """

    model = Message
    extra_context = {'title': 'Письма'}

    def get_queryset(self):
        """
        Метод возвращает список сообщений согласно правам доступа,
        если пользователь не авторизован, то возвращает пустой список.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return get_messages_from_cache()
            if user.has_perm('message.can_view_messages'):
                return get_messages_from_cache()
            return get_messages_from_cache().filter(owner=user)
        return Message.objects.none()


class MessageDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер детальной информации о сообщении """

    model = Message
    extra_context = {'title': 'Детали письма'}

    def get_object(self, queryset=None):
        """
        Метод проверяет права доступа и если права на просмотр деталей сообщения есть,
        то возвращает объект сообщения, иначе создаёт ошибку доступа.

        :return: Объект с информацией о сообщении.
        """
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        if user.has_perm('message.view_message'):
            return obj
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер формы создания сообщения """

    model = Message
    fields = ('subject', 'body', )
    extra_context = {'title': 'Создание письма'}
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        """
        Метод проверяет валидность заполненной формы и заносит в поле owner текущего пользователя.

        :param form: Заполненная форма
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер формы изменения сообщения """

    model = Message
    fields = ('subject', 'body', )
    extra_context = {'title': 'Обновление письма'}
    success_url = reverse_lazy('message:message_list')

    def get_object(self, queryset=None):
        """
        Метод проверяет права доступа и если права на редактирование сообщения есть,
        то возвращает объект сообщения, иначе создаёт ошибку доступа

        :return: Объект с информацией о сообщении.
        """
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер удаления сообщения """
    model = Message
    extra_context = {'title': 'Удаление письма'}
    success_url = reverse_lazy('message:message_list')

    def get_object(self, queryset=None):
        """
        Метод проверяет права доступа и если права на удаление сообщения есть,
        то возвращает объект сообщения, иначе создаёт ошибку доступа

        :return: Объект с информацией о сообщении.
        """
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied
