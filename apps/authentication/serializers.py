from rest_framework import serializers

from apps.authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "mobile",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create(mobile=validated_data["mobile"])
        user.set_password(validated_data["password"])
        user.save()
        return user
