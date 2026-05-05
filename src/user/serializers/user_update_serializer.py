from rest_framework import serializers

from user.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
        )
