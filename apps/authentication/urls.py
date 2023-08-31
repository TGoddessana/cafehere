from django.urls import include, path
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.authentication import views

urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
]
