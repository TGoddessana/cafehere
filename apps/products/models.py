from django.core.validators import MinValueValidator
from django.db import models

from core.utils.hangeul import get_initial_consonant
from core.utils.models import TimeStampedMixin, UUID4Mixin


class Category(UUID4Mixin):
    name = models.CharField(max_length=30)
    cafe = models.ForeignKey(
        "cafes.Cafe",
        on_delete=models.CASCADE,
        related_name="categories",
    )  # 카페가 삭제되면, 카페가 가지고 있는 카테고리들도 모두 삭제됩니다.

    class Meta:
        verbose_name_plural = "categories"
        # 카페 안에서 생성되는 카테고리들은 중복된 이름을 가질 수 없습니다.
        constraints = [
            models.UniqueConstraint(
                fields=["name", "cafe"],
                name="unique_category_per_cafe",
            )
        ]

    def __str__(self):
        return f"Category {self.name}"


class OptionGroup(UUID4Mixin):
    """
    옵션 그룹을 나타내는 모델입니다. 옵션 그룹은 여러 옵션들을 가질 수 있습니다.
    한 카페 안에서는, 옵션 그룹의 이름은 유일해야 합니다.

    예를 들면, "사이즈" 옵션 그룹에는 "small", "medium", "large" 옵션이 존재할 수 있습니다.
    """

    name = models.CharField(max_length=30)
    cafe = models.ForeignKey(
        "cafes.Cafe",
        on_delete=models.CASCADE,
        related_name="option_groups",
    )  # 카페가 삭제되면, 카페가 가지고 있는 옵션 그룹들도 모두 삭제됩니다.

    class Meta:
        # 카페 안에서 생성되는 옵션 그룹들은 중복된 이름을 가질 수 없습니다.
        constraints = [
            models.UniqueConstraint(
                fields=["name", "cafe"],
                name="unique_option_group_per_cafe",
            )
        ]

    def __str__(self):
        return f"OptionGroup {self.name}"


class Option(models.Model):
    name = models.CharField(max_length=30)
    add_price = models.IntegerField(validators=[MinValueValidator(0)])

    # 옵션 그룹이 삭제되면, 옵션 그룹이 가지고 있는 옵션들도 모두 삭제됩니다.
    option_group = models.ForeignKey(
        OptionGroup, on_delete=models.CASCADE, related_name="options"
    )

    class Meta:
        # 옵션 그룹 안에서 생성되는 옵션들은 중복된 이름을 가질 수 없습니다.
        constraints = [
            models.UniqueConstraint(
                fields=["name", "option_group"],
                name="unique_option_per_option_group",
            )
        ]

    def __str__(self):
        return f"Option {self.name}"


class Product(UUID4Mixin, TimeStampedMixin):
    name = models.CharField(max_length=30)
    description = models.TextField()
    cost = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.IntegerField(validators=[MinValueValidator(0)])
    expireation_date = models.DateTimeField()
    initial_consonant = models.CharField(
        max_length=30, editable=False
    )  # 초성 필드. 한글이 입력되면 자동으로 초성이 저장됩니다.
    barcode = models.ImageField(
        upload_to="products/barcodes", blank=True, null=True
    )  # 바코드 이미지 필드.
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    option_groups = models.ManyToManyField(OptionGroup, blank=True)

    @property
    def cafe(self):
        return self.category.cafe

    class Meta:
        # 카테고리 안에서 생성되는 상품 타입들은 중복된 이름을 가질 수 없습니다.
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_product_per_category"
            )
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.initial_consonant = get_initial_consonant(self.name)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"Product {self.name}"
