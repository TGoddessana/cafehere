from rest_framework import serializers

from apps.cafes.urls import CAFE_URL_KEYWORD
from apps.products.models import Category, OptionGroup, Product


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source="products.count", read_only=True)
    products = serializers.SlugRelatedField(
        slug_field="name", many=True, read_only=True
    )

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "products",
            "products_count",
        )
        read_only_fields = ("products",)


class ProductListSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=30, write_only=True)
    cost = serializers.IntegerField(write_only=True)
    expireation_date = serializers.DateTimeField(write_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    category_name = serializers.CharField(source="category.name", read_only=True)
    option_groups = serializers.PrimaryKeyRelatedField(
        queryset=OptionGroup.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "cost",
            "price",
            "expireation_date",
            "category",
            "category_name",
            "option_groups",
        )

    # 선택할 수 있는 카테고리는 해당 카페의 카테고리들이어야 합니다.
    def validate_category(self, value):
        cafe_uuid = self.context["request"].parser_context["kwargs"][CAFE_URL_KEYWORD]
        if value not in Category.objects.filter(cafe__uuid=cafe_uuid):
            raise serializers.ValidationError(
                "You can only select categories for that cafe."
            )
        return value

    # 선택할 수 있는 옵션 그룹은 해당 카테고리의 옵션 그룹들이어야 합니다.
    def validate_option_groups(self, value):
        cafe_uuid = self.context["request"].parser_context["kwargs"][CAFE_URL_KEYWORD]
        for option_group in value:
            if option_group not in OptionGroup.objects.filter(cafe__uuid=cafe_uuid):
                raise serializers.ValidationError(
                    "You can only select option groups for that cafe."
                )
        return value


class ProductDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=30)
    cost = serializers.IntegerField()
    price = serializers.IntegerField()
    expireation_date = serializers.DateTimeField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    option_groups = serializers.PrimaryKeyRelatedField(
        queryset=OptionGroup.objects.all(), many=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "cost",
            "price",
            "expireation_date",
            "category_name",
            "option_groups",
        )
