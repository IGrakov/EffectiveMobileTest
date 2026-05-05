from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeated = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "password",
            "password_repeated",
        )

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_repeated"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data: dict) -> User:
        validated_data.pop("password_repeated")
        return User.objects.create_user(**validated_data)
