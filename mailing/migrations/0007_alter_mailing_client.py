# Generated by Django 4.2.2 on 2024-05-18 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_owner'),
        ('mailing', '0006_alter_mailing_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='client',
            field=models.ManyToManyField(to='client.client', verbose_name='Клиенты'),
        ),
    ]