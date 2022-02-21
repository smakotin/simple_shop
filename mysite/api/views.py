from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions, AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.serializers import ProductListSerializer, ProductRetrieveSerializer, ProductCreateSerializer, \
    CartSerializer, AddProductCartSerializer, UpdateProductCartSerializer, DeleteProductCartSerializer, \
    ProductDiscountSerializer
from cart.models import ProductInCart, Cart
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
        try:  # TODO catch exception
            serializer.save(product_id=product_id, cart_id=cart_id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            Response(status=status.HTTP_406_NOT_ACCEPTABLE)


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

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ListAPICart(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ProductInCart.objects.filter(cart__user=user).annotate(
            product_price=F('product__price'),
            amount_with_discount=(
                    F('count') * F('product__price') * (100 - F('product__discount')) / 100
            ),
            amount_without_discount=(F('count') * (F('product__price'))),
        )
        return queryset

    def get_serializer_context(self):
        total_cart_sum = ProductInCart.objects.filter(cart__user=self.request.user).annotate(
            amount_with_discount=(
                    F('count') * F('product__price') * (100 - F('product__discount')) / 100
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
