from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое статьи")
    image = models.ImageField(upload_to='images/', verbose_name="Изображение", **NULLABLE)
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    def __str__(self):
        return self.title

    def count_of_views(self):
        self.views += 1
        self.save()


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('title',)
