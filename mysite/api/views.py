from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions, AllowAny
from rest_framework.response import Response

from api.serializers import ProductListSerializer, ProductRetrieveSerializer, ProductCreateSerializer, \
    CartSerializer, AddProductCartSerializer, UpdateProductCartSerializer
from cart.models import ProductInCart, Cart
from shop.models import Product

User = get_user_model()


class ListAPIProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class RetrieveAPIProduct(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [AllowAny]


class CreateAPIProduct(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = Product.objects


class UpdateApiProduct(RetrieveUpdateAPIView):
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.all()
    permission_classes = [DjangoModelPermissions]


class DeleteApiProduct(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [DjangoModelPermissions]


class AddProductCartAPI(CreateAPIView):
    serializer_class = AddProductCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        product_id = kwargs['pk']
        cart_id = self.request.COOKIES.get('cart')
        if cart_id is None:
            if user.is_authenticated:
                cart_id = Cart.objects.filter(user_id=user.pk).first().pk
        serializer.save(product_id=product_id, cart_id=cart_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateProductCartAPI(RetrieveUpdateAPIView):
    serializer_class = UpdateProductCartSerializer
    lookup_field = "product_id"

    def get_queryset(self):
        user = self.request.user
        cart_id = self.request.COOKIES.get('cart')
        product_id = self.kwargs['product_id']
        if cart_id is None:
            if user.is_authenticated:
                cart_id = Cart.objects.filter(user_id=user.pk).first().pk
            else:
                return ProductInCart.objects.none()
        return ProductInCart.objects.filter(product_id=product_id)#TODO check logic


class ListAPICart(ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProductInCart.objects.filter(cart__user=user)
        else:
            return ProductInCart.objects.all()
