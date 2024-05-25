# Generated by Django 4.2.2 on 2024-05-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_alter_mailing_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ('id',), 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AlterField(
            model_name='mailing',
            name='mailing_status',
            field=models.CharField(blank=True, choices=[('C', 'Создана'), ('R', 'Запущена'), ('S', 'Остановлена'), ('E', 'Завершена')], default='C', max_length=1, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='periodicity',
            field=models.CharField(blank=True, choices=[('D', 'Раз в день'), ('W', 'Раз в неделю'), ('M', 'Раз в месяц')], default='D', max_length=1, null=True, verbose_name='Периодичность'),
        ),
    ]
