import secrets

from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy

from config import settings
from .forms import UserRegisterForm, UserProfileForm, UserForgotPasswordForm
from .models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'title': 'Вход'}


class UserLogoutView(LogoutView):
    pass


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    extra_context = {'title': 'Профиль'}


class UserForgotPasswordView(TemplateView):
    template_name = 'users/password_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {'title': 'Забыли пароль'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForgotPasswordForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        user_email = form.cleaned_data['email']
        check_user = User.objects.get(email=user_email)
        new_password = secrets.token_hex(8)
        self.send_new_password(user_email, new_password)
        check_user.set_password(new_password)
        check_user.save()
        return redirect('users:login')

    def form_invalid(self, form):
        return self.render_to_response({'form': form, 'title': self.extra_context['title']})

    @staticmethod
    def send_new_password(to_email, password):
        send_mail(
            subject='Восстановление пароля',
            message=f'Новый пароль: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email]
        )
