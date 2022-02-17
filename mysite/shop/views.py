from django.views.generic import ListView

from shop.models import Product



class HomeShop(ListView):
    model = Product
    template_name = 'shop/index.html'





# class ProductRetrieveAPI(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductRetrieveSerializer



