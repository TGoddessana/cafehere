from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.cafes.models import Cafe


class CafeSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cafe
        fields = (
            "uuid",
            "name",
            "owner",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Cafe.objects.all(), fields=["name", "owner"]
            )
        ]
