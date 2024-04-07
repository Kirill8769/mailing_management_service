from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'



