# Generated by Django 5.0.4 on 2024-04-07 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_mailing_client_remove_mailing_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Почта'),
        ),
    ]