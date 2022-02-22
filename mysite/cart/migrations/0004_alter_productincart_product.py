# Generated by Django 4.0.2 on 2022-02-21 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_promocode_promocode_promo_code'),
        ('cart', '0003_alter_cart_user_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productincart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_product_in_cart', to='shop.product'),
        ),
    ]