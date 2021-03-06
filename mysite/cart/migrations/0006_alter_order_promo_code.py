# Generated by Django 4.0.2 on 2022-02-24 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_promocode_promocode_promo_code'),
        ('cart', '0005_order_final_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo_code_order', to='shop.promocode'),
        ),
    ]
