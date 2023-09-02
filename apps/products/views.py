from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.cafes.models import Cafe
from apps.cafes.urls import CAFE_URL_KEYWORD
from apps.products.filters import ProductFilter
from apps.products.models import Category, Product
from apps.products.permissions import IsCafeOwner
from apps.products.serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)

CATEGORY_TAG = "Category API"
PRODUCT_TAG = "Product API"


@extend_schema(
    tags=[CATEGORY_TAG],
)
class CategoryAPIViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsCafeOwner)

    def get_queryset(self):
        """
        두 가지 조건을 가지는 queryset을 반환합니다.
        1. 카페의 owner 이어야 합니다.
        2. 카페의 uuid 가 url 의 uuid 와 일치해야 합니다.
        """
        queryset = self.queryset.filter(
            cafe__uuid=self.kwargs[CAFE_URL_KEYWORD],
            cafe__owner=self.request.user,
        )
        return queryset

    def list(self, request, *args, **kwargs):
        """
        카페의 카테고리 목록을 조회합니다.
        """
        if not self.get_queryset():
            raise NotFound()
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(cafe=Cafe.objects.get(uuid=self.kwargs[CAFE_URL_KEYWORD]))


@extend_schema(
    tags=[PRODUCT_TAG],
)
class ProductAPIViewSet(ModelViewSet):
    lookup_url_kwarg = "product_id"
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (IsCafeOwner,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = self.queryset.filter(
            category__cafe__owner=self.request.user,
        )
        return queryset

    def get_serializer_class(self):
        if self.action == "list" or self.action == "create":
            return ProductListSerializer
        elif (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "delete"
        ):
            return ProductDetailSerializer
