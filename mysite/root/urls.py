from django.urls import path, include
from root.views import UserCreateAPIView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("register/", UserCreateAPIView.as_view()),
]