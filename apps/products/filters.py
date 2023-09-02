from django.db.models import Q
from django_filters import rest_framework as filters

from apps.products.models import Product


class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        lookup_expr="contains",
        label="Search",
    )
    category = filters.CharFilter(
        field_name="category__name",
        lookup_expr="exact",
        label="Category",
    )

    class Meta:
        model = Product
        fields = [
            "search",
            "category",
        ]

    @staticmethod
    def filter_search(queryset, name, value):
        """
        검색어 필터링 규칙을 지정합니다.
        - 이름 필드에 검색어가 포함되어 있거나
        - 초성 필드에 검색어가 포함되어 있으면
        검색어를 포함하는 Product 목록을 반환합니다.
        """
        return queryset.filter(
            Q(name__icontains=value) | Q(initial_consonant__icontains=value)
        )
