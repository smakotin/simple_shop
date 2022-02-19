from django.db.migrations import serializer
from django.db.models import F
from django.http import response
from rest_framework.relations import HyperlinkedIdentityField, StringRelatedField
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Serializer, IntegerField, \
    RelatedField

from cart.models import ProductInCart, Cart
from shop.models import Product



class ProductListSerializer(HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField('product-retrieve')

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'detail')


class ProductRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image']


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image']


class CartSerializer(ModelSerializer):
    class Meta:
        model = ProductInCart
        fields = '__all__'


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
