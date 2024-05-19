from django import forms
from django.core.exceptions import ValidationError

from .models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'email', 'comment',)

    def clean_email(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        user = self.initial.get('user').pk

        if Client.objects.filter(email=email, owner=user).exclude(id=self.instance.id).exists():
            raise ValidationError("Этот email уже используется другим клиентом.")

        return email
