from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
)
from django.core.cache import cache
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreatePasswordRetypeSerializer):
    def validate(self, attrs):
        email = attrs.get("email")

        if not cache.get(f"otp_verified:{email}"):
            raise serializers.ValidationError(
                {"email": "You must verify your email before registration."}
            )

        print("verified")

        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data.get("email")
        cache.delete(f"otp_verified:{email}")
        print("deleted the flag")
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
