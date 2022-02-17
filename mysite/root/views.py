from rest_framework.generics import CreateAPIView
from root.serializers import UserSerializer
from shop.models import User


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

