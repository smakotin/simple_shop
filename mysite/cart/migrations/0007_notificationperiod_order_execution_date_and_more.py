# Generated by Django 4.0.2 on 2022-03-04 21:00

import cart.models
import cart.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_order_promo_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='execution_date',
            field=models.DateTimeField(default=cart.utils.default_date_order),
        ),
        migrations.AddField(
            model_name='order',
            name='notification',
            field=models.ForeignKey(default=cart.models.NotificationPeriod.get_default_notification_time, on_delete=django.db.models.deletion.SET_DEFAULT, to='cart.notificationperiod'),
        ),
    ]