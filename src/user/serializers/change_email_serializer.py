from rest_framework import serializers

from user.models import User


class ChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already in use")  # noqa: TRY003, EM101

        return value
