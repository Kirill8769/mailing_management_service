from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView

from .models import Message


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Все письма'}

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return Message.objects.all()
            if user.has_perm('message.can_view_messages'):
                return Message.objects.all()
            return Message.objects.filter(owner=user)
        return Message.objects.none()


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {'title': 'Детали письма'}

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        if user.has_perm('message.view_message'):
            return obj
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('subject', 'body', )
    extra_context = {'title': 'Создание письма'}
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('subject', 'body', )
    extra_context = {'title': 'Обновление письма'}
    success_url = reverse_lazy('message:message_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    extra_context = {'title': 'Удаление письма'}
    success_url = reverse_lazy('message:message_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied
