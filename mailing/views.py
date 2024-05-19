from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView

from .forms import MailingForm
from .models import Mailing, Log


class MailingListView(ListView):
    model = Mailing
    extra_context = {'title': 'Рассылки'}

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return Mailing.objects.all()
            if user.has_perm('mailing.can_view_mailings'):
                return Mailing.objects.all()
            return Mailing.objects.filter(owner=user)
        return Mailing.objects.none()


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    extra_context = {'title': 'Детали рассылки'}

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        if user.has_perm('mailing.view_mailing'):
            return obj
        raise PermissionDenied


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создание рассылки'}
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Обновление рассылки'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.object.pk])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    extra_context = {'title': 'Удаление рассылки'}
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if obj.owner == user or user.is_superuser:
            return obj
        raise PermissionDenied


class StatisticView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/statistic.html'
    extra_context = {'title': 'Статистика'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.has_perm('mailing.can_view_logs'):
                context['object_list'] = Log.objects.all()
            else:
                context['object_list'] = Log.objects.filter(owner=user)
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return Log.objects.all()
            if user.has_perm('mailing.can_view_logs'):
                return Log.objects.all()
            return Log.objects.filter(owner=user)
        return Log.objects.none()


def check_mailing_status(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.mailing_status == 'R':
        mailing.mailing_status = 'S'
    else:
        mailing.mailing_status = 'R'
    mailing.save()
    return redirect('mailing:mailing_list')
