from django.db.models import Sum, F
from rest_framework import request

from cart.models import ProductInCart
from shop.models import PromoCode


def check_promo_code(text_promo_code):
    try:
        checked_promo_code = PromoCode.objects.get(promo_code__iexact=text_promo_code)
    except PromoCode.DoesNotExist:
        return None
    if checked_promo_code.is_active:
        return checked_promo_code
    return None


def get_promo_code_percent(promo_code):
    try:
        return promo_code.promo_discount
    except AttributeError:
        return 0


def get_total_order_sum_with_discount_and_promo_code(request, promo_code_percent):
    total = ProductInCart.objects.filter(cart__user=request.user).annotate(
        amount_with_discount=(
                F('count') * F('product__price') * (1 - (F('product__discount') + promo_code_percent) / 100)
        )
    ).aggregate(total_cart=Sum('amount_with_discount'))['total_cart']
    return total


def get_total_order_sum_with_promo_code(request, promo_code_percent):
    cart = ProductInCart.objects.filter(cart__user=request.user)
    total_amount_products_without_discount = 0
    total_amount_products_with_discount = 0
    for item in cart.filter(product__discount=0):
        total_amount_products_without_discount += (item.count * item.product.price)

    for item in cart.exclude(product__discount=0):
        total_amount_products_with_discount += (item.count * item.product.price) * (1 - item.product.discount / 100)
    result = total_amount_products_without_discount * (1 - promo_code_percent / 100) + \
             total_amount_products_with_discount

    return result


def get_total_order_sum_without_promo_code(request):
    total = ProductInCart.objects.filter(cart__user=request.user).annotate(
        amount_with_discount=(
                F('count') * F('product__price') * (1 - F('product__discount') / 100)
        )
    ).aggregate(total_cart=Sum('amount_with_discount'))['total_cart']
    return total


def get_amount_products_with_discount(request):
    pass

# def get_amount_with_promo_code(amount):
#     pass
#     return amount_with_promo_code
