from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from shop.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="user_cart")
    products = models.ManyToManyField(Product, through='ProductInCart', blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User: {} cart".format(self.user)


class ProductInCart(models.Model):

    product = models.OneToOneField(Product, unique=True, on_delete=models.CASCADE, related_name='product_product_in_cart')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_product_in_cart')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'cart'], name='unique_product') #TODO why it doesn't work. Fix
        ]

