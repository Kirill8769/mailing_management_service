# Generated by Django 5.0.4 on 2024-05-12 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Почта'),
        ),
    ]