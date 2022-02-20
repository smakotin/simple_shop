from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions, AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.serializers import ProductListSerializer, ProductRetrieveSerializer, ProductCreateSerializer, \
    CartSerializer, AddProductCartSerializer, UpdateProductCartSerializer
from cart.models import ProductInCart, Cart
from shop.models import Product
from django.db.models import Sum, F, Prefetch, Count

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


class AddProductCartAPI(ListCreateAPIView):
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
        serializer.save(product_id=product_id, cart_id=cart_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


class ListAPICart(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ProductInCart.objects.filter(cart__user=user).annotate(
            total_sum=(F('count') * F('product__price'))
        )

        return queryset

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """

        total_cart_sum = ProductInCart.objects.filter(cart__user=self.request.user).annotate(
            total_sum=(F('count') * F('product__price'))
        ).aggregate(total_cart=Sum('total_sum'))['total_cart']
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'total_cart_sum': total_cart_sum,
        }


# class RetrieveCartApi(ListAPIView):
#     serializer_class = CartSerializer
#
#     def get_queryset(self, *args, **kwargs):
#         query_set = Cart.objects.filter(user=self.request.user).annotate(
#             total_sum=(Sum('cart_product_in_cart__count') * F('products__price'))
#         )
#         return query_set

    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #
    #     total_cart_sum = Cart.objects.filter(user=self.request.user).annotate(
    #         total_sum=(Sum('cart_product_in_cart__count') * Sum('products__price'))
    #     ).aggregate(total=Sum('total_sum'))['total']
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self,
    #         'total_cart_sum': total_cart_sum,
    #     }

