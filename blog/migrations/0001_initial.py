# Generated by Django 4.2.2 on 2024-05-19 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержимое статьи')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog', verbose_name='Изображение')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')),
                ('publication_date', models.DateField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
        ),
    ]
