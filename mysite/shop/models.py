from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(verbose_name='Телефон')
    email = models.EmailField(verbose_name='email address')
    REQUIRED_FIELDS = ['first_name', 'phone', 'last_name', 'email']


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    image = models.ImageField(verbose_name='Фото', upload_to='images/%Y/%m/', blank=True)
    discount = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        blank=True,
        validators=[
            MaxValueValidator(limit_value=99.99, message='Discount must be less than 100'),
            MinValueValidator(limit_value=0, message='Discount cannot be less than 0'),
        ]
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class PromoCode(models.Model):
    promo_code = models.CharField(max_length=20)
    expiration_date = models.DateField(default=date.today)
    promo_discount = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        blank=True,
        validators=[
            MaxValueValidator(limit_value=99.99, message='Discount must be less than 100'),
            MinValueValidator(limit_value=0, message='Discount cannot be less than 0'),
        ]
    )
    is_active = models.BooleanField(default=False)
    works_with_discount = models.BooleanField(default=False)

    def __str__(self):
        return self.promo_code
