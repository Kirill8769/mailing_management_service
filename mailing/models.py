from django.db import models
from django.utils import timezone

from client.models import Client
from message.models import Message
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    PERIOD_LIST = [
        ('D', 'Раз в день'),
        ('W', 'Раз в неделю'),
        ('M', 'Раз в месяц'),
    ]
    STATUS_LIST = [
        ('C', 'Создана'),
        ('R', 'Запущена'),
        ('S', 'Остановлена'),
        ('E', 'Завершена'),
    ]
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания', **NULLABLE)
    periodicity = models.CharField(max_length=1, choices=PERIOD_LIST, default='D', verbose_name='Периодичность', **NULLABLE)
    mailing_status = models.CharField(max_length=1, choices=STATUS_LIST, default='C', verbose_name='Статус', **NULLABLE)
    client = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ('id', )
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_view_mailings', 'can view mailings'),
            ('can_check_status_mailings', 'can check status mailings'),
        ]


class Log(models.Model):
    STATUS_LIST = [
        ('Y', 'Успешно'),
        ('N', 'Ошибка'),
    ]
    date_send = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата отправки')
    attempt_status = models.CharField(max_length=1, choices=STATUS_LIST, verbose_name='Статус', **NULLABLE)
    answer_server = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.mailing}: {self.client} - {self.attempt_status}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        permissions = [
            ('can_view_logs', 'can view logs'),
        ]
