# Generated by Django 5.0.4 on 2024-04-07 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0003_remove_mailing_client_remove_mailing_message_and_more'),
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('periodicity', models.CharField(blank=True, choices=[('D', 'Раз в день'), ('W', 'Раз в неделю'), ('M', 'Раз в месяц')], max_length=1, null=True, verbose_name='Периодичность')),
                ('mailing_status', models.CharField(blank=True, choices=[('C', 'Создана'), ('R', 'Запущена'), ('S', 'Остановлена'), ('E', 'Завершена')], max_length=1, null=True, verbose_name='Статус')),
                ('client', models.ManyToManyField(to='client.client', verbose_name='Клиент')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Рассылку',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_last_send', models.DateTimeField(verbose_name='Дата последней отправки')),
                ('attempt_status', models.CharField(blank=True, choices=[('Y', 'Успешно'), ('N', 'Не успешно')], max_length=1, null=True, verbose_name='Статус')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Попытку',
                'verbose_name_plural': 'Попытки',
            },
        ),
    ]
