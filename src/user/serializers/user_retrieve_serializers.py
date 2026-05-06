from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from user.models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "role",
            "email",
            "first_name",
            "middle_name",
            "last_name",
        )

    @extend_schema_field(
        serializers.ChoiceField(choices=("Admin", "Supervisor", "Manager", "Default")),
    )
    def get_role(self, obj: User) -> str:
        if obj.is_superuser:
            return "Admin"
        if obj.groups.filter(name="Admin").exists():
            return "Admin"
        if obj.groups.filter(name="Supervisor").exists():
            return "Supervisor"
        if obj.groups.filter(name="Manager").exists():
            return "Manager"
        return "Default"


class UserListSerializer(UserRetrieveSerializer):
    date_joined = serializers.DateTimeField(source="created_at", read_only=True, format="%Y-%m-%d")

    class Meta(UserRetrieveSerializer.Meta):
        fields = (
            *UserRetrieveSerializer.Meta.fields,
            "date_joined",
            "is_staff",
            "is_active",
        )
