from django.urls import path

from apps.cafes import views

CAFE_LIST_URL_NAME = "cafe-list"
CAFE_DETAIL_URL_NAME = "cafe-detail"
CAFE_URL_KEYWORD = "cafe_uuid"

urlpatterns = [
    path(
        "",
        views.CafeAPIViewSet.as_view({"get": "list", "post": "create"}),
        name=CAFE_LIST_URL_NAME,
    ),
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/",
        views.CafeAPIViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name=CAFE_DETAIL_URL_NAME,
    ),
]
