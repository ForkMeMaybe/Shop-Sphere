from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
)
from django.core.cache import cache
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreatePasswordRetypeSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        print(cache.get(f"otp_verified:{email}"))

        if not cache.get(f"otp_verified:{email}"):
            raise serializers.ValidationError(
                {
                    "email": "Skipping steps already? Love the confidence. Hate the execution. 💀"
                }
            )

        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data.get("email")
        cache.delete(f"otp_verified:{email}")
        return super().create(validated_data)

    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]
