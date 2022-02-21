from django.db.migrations import serializer
from django.db.models import F, Sum
from django.http import response
from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedIdentityField, StringRelatedField
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Serializer, IntegerField, \
    RelatedField, DecimalField, SerializerMethodField

from cart.models import ProductInCart, Cart, Order
from shop.models import Product


class ProductListSerializer(HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField('product-retrieve')

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'detail')


class ProductRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', "total_sum"]


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image']


class ProductDiscountSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('discount',)


class CartSerializer(ModelSerializer):
    product_title = CharField()
    product_price = DecimalField(max_digits=9, decimal_places=2)
    total = SerializerMethodField()
    amount_without_discount = DecimalField(max_digits=9, decimal_places=2)
    amount_with_discount = DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = ProductInCart
        fields = '__all__'
        extra_fields = (
            'product_title',
            'amount_without_discount', 'total', 'product_price',
            'amount_with_discount',

        )

    def get_total(self, obj):
        return self.context['total_cart_sum']


class AddProductCartSerializer(ModelSerializer):
    product_id = IntegerField(read_only=True)

    class Meta:
        model = ProductInCart
        fields = ['count', 'product_id', 'cart_id']


class UpdateProductCartSerializer(ModelSerializer):
    product_id = IntegerField(read_only=True)

    class Meta:
        model = ProductInCart
        fields = ['count', 'product_id', 'cart_id']


class DeleteProductCartSerializer(ModelSerializer):
    class Meta:
        model = ProductInCart
        fields = '__all__'


class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

