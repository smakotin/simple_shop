from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(verbose_name='Телефон')
    

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    image = models.ImageField(verbose_name='Фото', upload_to='images/%Y/%m/', blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Promocode(models.Model):
    promocode = models.CharField(max_length=20)
    expiration_date = models.DateField(default=date.today)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.promocode
