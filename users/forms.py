from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForgotPasswordForm(forms.Form):
    email = forms.EmailField(help_text='введите почту с которой ранее заходили на наш портал')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Указанный email не зарегистрирован')
        return email


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'is_active', 'email', 'password', 'first_name', 'last_name', 'is_active', 'avatar',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
