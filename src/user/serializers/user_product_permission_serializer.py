from rest_framework import serializers

from user.models import UserProductPermission


class UserProductPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductPermission

        fields = (
            "id",
            "user",
            "region",
            "permission",
            "is_allowed",
        )


class UserProductPermissionItemSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.code")

    class Meta:
        model = UserProductPermission

        fields = (
            "id",
            "user",
            "region",
            "permission",
            "is_allowed",
        )


class UserPermissionsResponseSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    permissions = UserProductPermissionItemSerializer(many=True)
