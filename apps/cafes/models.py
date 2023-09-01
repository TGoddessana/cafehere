from django.db import models

from core.utils.models import TimeStampedMixin, UUID4Mixin


class Cafe(UUID4Mixin, TimeStampedMixin):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="cafes"
    )

    class Meta:
        """
        유저별로 카페 이름은 유일해야 합니다.
        """

        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"], name="unique_cafe_name_per_user"
            ),
        ]

    def __str__(self):
        return f"Cafe {self.name}"
