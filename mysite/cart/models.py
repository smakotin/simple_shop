from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from cart.utils import default_date_order
from shop.models import Product, PromoCode

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    products = models.ManyToManyField(Product, through='ProductInCart', blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User: {} cart".format(self.user)


class ProductInCart(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_product_in_cart')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_product_in_cart')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'cart'], name='unique_product')
        ]


class NotificationPeriod(models.Model):
    minutes = models.PositiveIntegerField(unique=True)

    @classmethod
    def get_default_notification_time(cls):
        obj, created = cls.objects.get_or_create(minutes=30)
        return obj.pk

    def __str__(self):
        return f'notification period {self.minutes} minutes'
        
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    created_date = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(ProductInCart, on_delete=models.CASCADE, related_name='cart_order')
    text = models.TextField(max_length=1000, blank=True)
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='promo_code_order'
    )
    execution_date = models.DateTimeField(default=default_date_order)
    notification = models.ForeignKey(
        NotificationPeriod,
        on_delete=models.SET_DEFAULT,
        default=NotificationPeriod.get_default_notification_time
    )
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)




