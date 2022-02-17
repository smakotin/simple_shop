from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from root.serializers import UserSerializer
from cart.models import Cart
from shop.models import User


# class Register(CreateAPIView):
#     serializer_class = CreateUserSerializer
#     queryset = User.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         user_id = response.data['id']
#         cart = Cart.objects.get(user_id=user_id)
#         # TODO when we replace cart logic to signal
#         response.set_cookie("cart", cart.id)
#         return response

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user_id = response.data['id']
        cart = Cart.objects.get(user_id=user_id)
        # TODO when we replace cart logic to signal
        response.set_cookie("cart", cart.id)
        return response
