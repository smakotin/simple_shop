# Generated by Django 4.0.2 on 2022-02-20 21:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MaxValueValidator(limit_value=99.99, message='Discount must be less than 100'), django.core.validators.MinValueValidator(limit_value=0, message='Discount cannot be less than 0')]),
        ),
    ]
