from django.urls import path, include
from root.views import UserCreateAPIView, UserList, UserDetail

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("register/", UserCreateAPIView.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]