from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import DjangoModelPermissions, AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.serializers import ProductListSerializer, ProductRetrieveSerializer, ProductCreateSerializer, \
    CartSerializer, AddProductCartSerializer, UpdateProductCartSerializer, DeleteProductCartSerializer, \
    ProductDiscountSerializer, ClientOrderSerializer, CreateOrderSerializer
from api.utils import check_promo_code, get_promo_code_percent, get_total_order_sum_with_discount_and_promo_code, \
    get_total_order_sum_with_promo_code, get_total_order_sum_without_promo_code
from cart.models import ProductInCart, Cart, Order
from shop.models import Product
from django.db.models import Sum, F

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
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    queryset = Product.objects


class UpdateApiProduct(RetrieveUpdateAPIView):
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.all()
    permission_classes = [DjangoModelPermissions, IsAuthenticated]


class DeleteApiProduct(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]


class AddProductCartAPI(CreateAPIView):
    serializer_class = AddProductCartSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user_id=user.pk)
        cart_id = cart.pk
        return ProductInCart.objects.filter(cart_id=cart_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        product_id = kwargs['pk']
        cart, created = Cart.objects.get_or_create(user_id=user.pk)
        cart_id = cart.pk

        try:  # TODO catch exception
            serializer.save(product_id=product_id, cart_id=cart_id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class UpdateProductCartAPI(RetrieveUpdateAPIView):
    serializer_class = UpdateProductCartSerializer
    lookup_field = "product_id"
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        cart, created = Cart.objects.get_or_create(user_id=user.pk)
        cart_id = cart.pk
        return ProductInCart.objects.filter(cart_id=cart_id, product_id=product_id)

    def update(self, request, *args, **kwargs):
        if request.POST['count'] == '0':
            ProductInCart.objects.filter(product_id=kwargs['product_id']).delete()
            return Response(status=status.HTTP_200_OK)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ListAPICart(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ProductInCart.objects.filter(cart__user=user).annotate(
            product_title=F('product__title'),
            product_price=F('product__price'),
            amount_with_discount=(
                    F('count') * F('product__price') * (1 - F('product__discount') / 100)
            ),
            amount_without_discount=(F('count') * (F('product__price'))),
        )
        return queryset

    def get_serializer_context(self):
        total_cart_sum = ProductInCart.objects.filter(cart__user=self.request.user).annotate(
            amount_with_discount=(
                    F('count') * F('product__price') * (1 - F('product__discount') / 100)
            )
        ).aggregate(total_cart=Sum('amount_with_discount'))['total_cart']
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'total_cart_sum': total_cart_sum,
        }


class DeleteProductCartApi(RetrieveDestroyAPIView):
    queryset = ProductInCart.objects
    serializer_class = DeleteProductCartSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]


class ProductDiscountApi(RetrieveUpdateAPIView):
    queryset = Product.objects
    serializer_class = ProductDiscountSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]


class ActivatePromoCodeApi(RetrieveAPIView):
    pass


class CreateOrderApi(CreateAPIView):
    queryset = Order.objects
    serializer_class = ClientOrderSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = request.user.user_cart.first().cart_product_in_cart.first()
        promo_code_text = serializer.validated_data['promo_code_text']
        checked_promo_code = check_promo_code(promo_code_text)
        promo_code_percent = get_promo_code_percent(checked_promo_code)
        if checked_promo_code:
            if checked_promo_code.works_with_discount:
                total_order_sum = get_total_order_sum_with_discount_and_promo_code(request, promo_code_percent)
            if not checked_promo_code.works_with_discount:
                total_order_sum = get_total_order_sum_with_promo_code(request, promo_code_percent)
        else:
            total_order_sum = get_total_order_sum_without_promo_code(request)

        kwargs = dict(
            user_id=request.user.id,
            cart_id=cart.id,
            text=serializer.validated_data['text'],
            promo_code=checked_promo_code
        )
        kwargs.update(final_amount=total_order_sum)
        order = Order.objects.create(**kwargs)
        serializer = CreateOrderSerializer(instance=order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
