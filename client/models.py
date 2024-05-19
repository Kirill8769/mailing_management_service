from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        permissions = [
            ('can_view_clients', 'can view clients'),
        ]
