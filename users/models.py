from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    country = models.CharField(max_length=100, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)

    USERNAME_FIELD = "email"
    username = USERNAME_FIELD
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)


class Payments(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH = "Наличные", "Наличные"
        TRANSFER = "Перевод", "Перевод"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользватель', **NULLABLE)
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', default=datetime.now())
    paid_course = models.ForeignKey(Course, verbose_name='Название курса', on_delete=models.CASCADE)
    payment_amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, default=PaymentMethod.CASH,
                                      choices=PaymentMethod, verbose_name='Метод оплаты')
    payment_link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)
    payment_id = models.CharField(max_length=255, verbose_name='ID платежа', **NULLABLE)

    def __str__(self):
        return str(self.paid_course)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('id',)
