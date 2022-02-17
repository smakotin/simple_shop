from django.urls import path

from api.views import RetrieveAPIProduct, ListAPIProduct, CreateAPIProduct, AddProductCartAPI, ListAPICart, \
    UpdateApiProduct, DeleteApiProduct, UpdateProductCartAPI

urlpatterns = [
    path('products/', ListAPIProduct.as_view(), name="product-list"),
    path('products/<int:pk>', RetrieveAPIProduct.as_view(), name="product-retrieve"),
    path('add_product/', CreateAPIProduct.as_view(), name="add-product"),
    path('update_product/<int:pk>', UpdateApiProduct.as_view(), name="update-product"),
    path('delete_product/<int:pk>', DeleteApiProduct.as_view(), name="delete-product"),
    path('cart/', ListAPICart.as_view(), name="cart-list"),
    path('cart/add/<int:pk>/', AddProductCartAPI.as_view(), name="add-to-cart"),
    path('cart/change/<int:product_id>/', UpdateProductCartAPI.as_view(), name="update-in-cart"),
]

