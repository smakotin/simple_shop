from django.urls import path

from api.views import RetrieveAPIProduct, ListAPIProduct, CreateAPIProduct, AddProductCartAPI, \
    UpdateApiProduct, DeleteApiProduct, UpdateProductCartAPI, ListAPICart, DeleteProductCartApi, \
    ProductDiscountApi, ActivatePromoCodeApi, CreateOrderApi

urlpatterns = [
    path('products/', ListAPIProduct.as_view(), name="product-list"),
    path('products/<int:pk>', RetrieveAPIProduct.as_view(), name="product-retrieve"),
    path('add_product/', CreateAPIProduct.as_view(), name="add-product"),
    path('update_product/<int:pk>', UpdateApiProduct.as_view(), name="update-product"),
    path('delete_product/<int:pk>', DeleteApiProduct.as_view(), name="delete-product"),

    path('cart/', ListAPICart.as_view(), name="cart-list"),
    path('cart/add/<int:pk>/', AddProductCartAPI.as_view(), name="add-to-cart"),
    path('cart/change/<int:product_id>/', UpdateProductCartAPI.as_view(), name="update-in-cart"),
    path('cart/delete_product/<int:pk>/', DeleteProductCartApi.as_view(), name="delete-in-cart"),
    path('cart/activate_promo_code/', ActivatePromoCodeApi.as_view(), name="activate-promo_code"),
    path('cart/create_order/', CreateOrderApi.as_view(), name="create_order"),

    path('products/add_discount/<int:pk>/', ProductDiscountApi.as_view(), name="add-discount"),
]

