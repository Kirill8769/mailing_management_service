from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog', blank=True, null=True, verbose_name='Изображение')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    publication_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id', )
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
