from typing import Any, ClassVar

from rest_framework import serializers

from user.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "password",
        )
        extra_kwargs: ClassVar[dict[str, Any]] = {
            "password": {"write_only": True},
        }
