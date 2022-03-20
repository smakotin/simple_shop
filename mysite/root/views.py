import requests
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from root.serializers import UserSerializer
from shop.models import User


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ActivateUserByEmail(APIView):

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}

        url = 'http://localhost:8000/auth/users/activation/'
        response = requests.post(url, data=payload)
        if response.ok:
            return HttpResponse('Thank you! Your account has been activated!')
        else:
            return HttpResponse(f'{response.text}')


