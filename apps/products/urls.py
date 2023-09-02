from django.urls import path

from apps.cafes.urls import CAFE_URL_KEYWORD
from apps.products import views

CATEGORY_LIST_URL_NAME = "category-list"
CATEGORY_DETAIL_URL_NAME = "category-detail"
CATEGORY_URL_KEYWORD = "category_id"

OPTION_GROUP_LIST_URL_NAME = "optiongroup-list"
OPTION_GROUP_DETAIL_URL_NAME = "optiongroup-detail"
OPTION_GROUP_URL_KEYWORD = "optiongroup_id"

PRODUCT_LIST_URL_NAME = "product-list"
PRODUCT_DETAIL_URL_NAME = "product-detail"
PRODUCT_URL_KEYWORD = "product_id"

urlpatterns = [
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/categories/",
        views.CategoryAPIViewSet.as_view({"get": "list", "post": "create"}),
        name=CATEGORY_LIST_URL_NAME,
    ),
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/categories/<int:{CATEGORY_URL_KEYWORD}>/",
        views.CategoryAPIViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name=CATEGORY_DETAIL_URL_NAME,
    ),
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/optiongroups/",
        views.OptionGroupAPIViewSet.as_view({"get": "list", "post": "create"}),
        name=OPTION_GROUP_LIST_URL_NAME,
    ),
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/optiongroups/<int:{OPTION_GROUP_URL_KEYWORD}>/",
        views.OptionGroupAPIViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/products/",
        views.ProductAPIViewSet.as_view({"get": "list", "post": "create"}),
        name=PRODUCT_LIST_URL_NAME,
    ),
    path(
        f"<uuid:{CAFE_URL_KEYWORD}>/products/<int:{PRODUCT_URL_KEYWORD}>/",
        views.ProductAPIViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name=PRODUCT_DETAIL_URL_NAME,
    ),
]
