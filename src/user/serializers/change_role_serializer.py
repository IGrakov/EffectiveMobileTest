from rest_framework import serializers

from user import constants


class ChangeRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=constants.Roles.choices)
