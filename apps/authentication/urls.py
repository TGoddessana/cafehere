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
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("refresh/", views.RefreshAPIVIew.as_view(), name="refresh"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
]
