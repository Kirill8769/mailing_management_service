import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy

from config import settings
from .forms import UserRegisterForm, UserProfileForm, UserForgotPasswordForm
from .models import User
from client.models import Client
from mailing.models import Mailing
from message.models import Message


class UserListView(LoginRequiredMixin, ListView):
    """ Контроллер списка пользователей """

    model = User
    extra_context = {'title': 'Пользователи сервиса'}

    def get_context_data(self, **kwargs):
        """ Метод заполняет информационные данные о пользователях """

        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['is_moderator'] = user.groups.filter(name='moderator').exists()
        context['is_superuser'] = user.is_superuser

        users = self.get_queryset()
        user_data_list = []
        for user_obj in users:
            user_data = {
                'user': user_obj,
                'mailing_count': Mailing.objects.filter(owner=user_obj).count(),
                'active_mailing_count': Mailing.objects.filter(owner=user_obj, mailing_status='R').count(),
                'message_count': Message.objects.filter(owner=user_obj).count(),
                'client_count': Client.objects.filter(owner=user_obj).count(),
            }
            user_data_list.append(user_data)
        context['user_data_list'] = user_data_list

        return context

    def get_queryset(self):
        """ Метод возвращает список пользователей согласно правам доступа. """

        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return User.objects.exclude(is_superuser=True)
            if user.groups.filter(name='moderator').exists():
                return User.objects.exclude(is_superuser=True).exclude(id=user.pk)
        raise PermissionDenied


class UserLoginView(LoginView):
    """ Контроллера входа в личный кабинет """

    template_name = 'users/login.html'
    extra_context = {'title': 'Вход'}


class UserLogoutView(LogoutView):
    """ Контроллера выхода из личного кабинета """
    pass


class UserCreateView(CreateView):
    """ Контроллер формы регистрации """

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        """
        Проверяет валидность заполненной формы, генерирует и записывает токен данные пользователя и
        отправляет письмо со ссылкой для верификации на указанную почту.
        """

        user = form.save()
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user.token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке\n{url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """ Контроллер формы редактирования профиля пользователя """

    model = User
    form_class = UserProfileForm
    extra_context = {'title': 'Профиль'}
    success_url = reverse_lazy('main:index')


class UserForgotPasswordView(TemplateView):
    """ Контроллер формы восстановления пароля пользователя """

    template_name = 'users/password_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {'title': 'Забыли пароль'}

    def get_context_data(self, **kwargs):
        """ Метод передаёт в шаблон форму для восстановления пароля. """

        context = super().get_context_data(**kwargs)
        context['form'] = UserForgotPasswordForm()
        return context

    def post(self, request, *args, **kwargs):
        """ Проверяет валидность заполненной формы. """

        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """ Генерирует и записывает новый пароль, и отправляет его пользователю на указанную почту. """

        user_email = form.cleaned_data['email']
        check_user = User.objects.get(email=user_email)
        new_password = secrets.token_hex(8)
        self.send_new_password(user_email, new_password)
        check_user.set_password(new_password)
        check_user.save()
        return redirect('users:login')

    def form_invalid(self, form):
        """ Обрабатывает некорректное заполнение формы """

        return self.render_to_response({'form': form, 'title': self.extra_context['title']})

    @staticmethod
    def send_new_password(to_email, password):
        """ Метод для отправки писем при восстановлении пароля """

        send_mail(
            subject='Восстановление пароля',
            message=f'Новый пароль: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email]
        )


def email_verification(request, token):
    """ Активация пользователя при успешной верификации """

    user = get_object_or_404(User, token=token)
    if user:
        user.is_active = True
        user.save()
    return redirect(reverse('users:login'))


def change_status(request, pk):
    """ Смена статуса активности пользователя """

    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:users-list'))
