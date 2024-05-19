from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(
        upload_to='users/avatars/', **NULLABLE, verbose_name='аватар', help_text='Загрузите аватар'
    )
    token = models.CharField(max_length=100, **NULLABLE, verbose_name='токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_check_active_users', 'can check active users'),
        ]
