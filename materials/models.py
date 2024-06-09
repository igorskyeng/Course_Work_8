from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    course_name = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='materials/', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    amount = models.IntegerField(default=1000, verbose_name='Цена')

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('id',)


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=150, verbose_name='Название урока')
    course = models.ForeignKey(Course, verbose_name='Название курса', on_delete=models.CASCADE, **NULLABLE)
    preview = models.ImageField(upload_to='materials/', verbose_name='Изображение', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    link_to_the_video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Подписавшийся пользователь',
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Курс для подписки', on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
