from django.urls import path

from apps.cafes import views

urlpatterns = [
    path("cafes/", views.hello_cafe, name="cafes"),
]
