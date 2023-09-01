from django.urls import path

from apps.cafes import views

urlpatterns = [
    path(
        "cafes/",
        views.CafeAPIViewSet.as_view({"get": "list", "post": "create"}),
        name="cafe-list",
    ),
    path(
        "cafes/<uuid:uuid>/",
        views.CafeAPIViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="cafe-detail",
    ),
]
