from django.db import models

from users.models import User


class Message(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
