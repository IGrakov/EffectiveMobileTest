from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError({"password": "New password must be different from the old password"})

        validate_password(attrs["new_password"])
        return attrs
