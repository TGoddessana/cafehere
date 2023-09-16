from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.cafes.urls import CAFE_URL_KEYWORD
from apps.products.models import Category, Option, OptionGroup, Product


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source="products.count", read_only=True)
    products = serializers.SlugRelatedField(
        slug_field="name", many=True, read_only=True
    )

    class Meta:
        model = Category
        fields = (
            "uuid",
            "name",
            "products",
            "products_count",
        )
        read_only_fields = ("products",)

    def validate_name(self, value):
        """
        카테고리 이름은 해당 카페에서 유일해야 합니다.
        """
        if self.context["request"]._request.method == "POST":
            cafe_uuid = self.context["request"].parser_context["kwargs"][
                CAFE_URL_KEYWORD
            ]
            if Category.objects.filter(cafe__uuid=cafe_uuid, name=value).exists():
                raise serializers.ValidationError(_("Category name must be unique."))
        return value


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            "name",
            "add_price",
        )


class OptionGroupSerializer(serializers.ModelSerializer):
    options_count = serializers.IntegerField(source="options.count", read_only=True)
    options = OptionSerializer(many=True)

    class Meta:
        model = OptionGroup
        fields = (
            "id",
            "name",
            "options",
            "options_count",
        )
        read_only_fields = ("options",)

    @transaction.atomic
    def create(self, validated_data):
        options_data = validated_data.pop("options")
        option_group = OptionGroup.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(
                name=option_data["name"],
                add_price=option_data["add_price"],
                option_group=option_group,
            )
        return option_group

    @transaction.atomic
    def update(self, instance, validated_data):
        options_data = validated_data.pop("options")
        instance.name = validated_data.get("name", instance.name)
        # 인스턴스가 가지고 있는 옵션보다 새로 들어온 옵션의 개수가 적으면,
        # 그것은 옵션을 삭제하겠다는 것을 의미
        if len(instance.options.all()) > len(options_data):
            for previous_option in instance.options.all():
                if previous_option.name not in [item["name"] for item in options_data]:
                    previous_option.delete()
        # 인스턴스가 가지고 있는 옵션보다 새로 들어온 옵션의 개수가 많으면,
        # 그것은 옵션을 추가하겠다는 것을 의미
        else:
            for item in options_data:
                obj, created = Option.objects.update_or_create(
                    name=item["name"],
                    add_price=item["add_price"],
                    option_group=instance,
                )
        instance.save()
        return instance

    def validate_name(self, value):
        """
        옵션 그룹 이름은 해당 카페에서 유일해야 합니다.
        """
        if self.context["request"]._request.method == "POST":
            cafe_uuid = self.context["request"].parser_context["kwargs"][
                CAFE_URL_KEYWORD
            ]
            if OptionGroup.objects.filter(cafe__uuid=cafe_uuid, name=value).exists():
                raise serializers.ValidationError(
                    _("Option group name must be unique.")
                )
        return value


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

    def validate_category(self, value):
        """
        카테고리는 해당 카페의 카테고리여야 합니다.
        """
        cafe_uuid = self.context["request"].parser_context["kwargs"][CAFE_URL_KEYWORD]
        if value not in Category.objects.filter(cafe__uuid=cafe_uuid):
            raise serializers.ValidationError(
                _("You can only select categories for that cafe.")
            )
        return value

    def validate_option_groups(self, value):
        """
        선택할 수 있는 옵션 그룹은 해당 카테고리의 옵션 그룹들이어야 합니다.
        """
        cafe_uuid = self.context["request"].parser_context["kwargs"][CAFE_URL_KEYWORD]
        for option_group in value:
            if option_group not in OptionGroup.objects.filter(cafe__uuid=cafe_uuid):
                raise serializers.ValidationError(
                    _("You can only select option groups for that cafe.")
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
            "category_name",
            "option_groups",
        )
