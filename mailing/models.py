from django.db import models
from django.utils import timezone

from client.models import Client
from message.models import Message

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
    title = models.CharField(max_length=150, verbose_name='Заголовок', **NULLABLE)
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания', **NULLABLE)
    periodicity = models.CharField(max_length=1, choices=PERIOD_LIST, verbose_name='Периодичность', **NULLABLE)
    mailing_status = models.CharField(max_length=1, choices=STATUS_LIST, verbose_name='Статус', **NULLABLE)
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.client}: {self.mailing_status}'

    class Meta:
        verbose_name = 'Рассылку'
        verbose_name_plural = 'Рассылки'


class Attempt(models.Model):
    STATUS_LIST = [
        ('Y', 'Успешно'),
        ('N', 'Не успешно'),
    ]
    date_send = models.DateTimeField(auto_now_add=timezone.now, **NULLABLE, verbose_name='Дата отправки')
    attempt_status = models.CharField(max_length=1, choices=STATUS_LIST, verbose_name='Статус', **NULLABLE)
    answer_server = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.mailing}: {self.client} - {self.attempt_status}'

    class Meta:
        verbose_name = 'Попытку'
        verbose_name_plural = 'Попытки'