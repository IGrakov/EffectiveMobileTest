from rest_framework import serializers


class ChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()
