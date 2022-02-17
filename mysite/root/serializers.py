from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField, IntegerField
from rest_framework.serializers import Serializer, ModelSerializer
from cart.models import Cart
from django.contrib.auth import get_user_model


User = get_user_model()


# class CreateUserSerializer(Serializer):
#
#     username = CharField(required=True)
#     first_name = CharField(required=False, default="")
#     last_name = CharField(required=False, default="")
#     email = EmailField(required=True)
#     phone = CharField(required=False)
#
#     password_1 = CharField(required=True, write_only=True)
#     password_2 = CharField(required=True, write_only=True)
#
#     id = IntegerField(read_only=True)
#
#     def validate(self, attrs):
#         if attrs['password_1'] != attrs['password_2']:
#             raise ValidationError(detail="password must be equals")
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data["username"],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             email=validated_data['email'],
#             phone=validated_data.get('phone'),
#             password=validated_data['password_1']
#         )
#         Cart.objects.create(user=user)
#         # TODO replace this logic to signal
#         return user

class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


