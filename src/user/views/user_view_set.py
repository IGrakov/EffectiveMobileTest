from typing import ClassVar, Iterable

from django.contrib.auth.models import Group
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.permissions import CanManageUser, IsAdmin
from user.serializers import (
    ChangeRoleSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)


class UserViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    serializer_classes: ClassVar[dict[str, type[BaseSerializer]]] = {
        "list": UserListSerializer,
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
        "change_role": ChangeRoleSerializer,
    }

    def get_serializer_class(self) -> type[BaseSerializer]:
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_permissions(self) -> Iterable[BasePermission]:
        if self.action == "create":
            return (AllowAny(),)

        if self.action == "list":
            return (IsAdmin(),)

        if self.action in ["retrieve", "update", "partial_update", "destroy", "change_role"]:
            return IsAuthenticated(), CanManageUser()

        return (IsAuthenticated(),)

    def perform_destroy(self, instance: User) -> None:
        instance.is_active = False
        instance.save()

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()

        if self.request.user.is_superuser:
            return qs

        return qs.filter(is_superuser=False)

    @extend_schema(
        request=ChangeRoleSerializer,
        responses={
            200: inline_serializer(
                name="ChangeRoleResponse",
                fields={
                    "detail": serializers.CharField(),
                },
            ),
        },
    )
    @action(detail=True, methods=["patch"], url_path="change-role")
    def change_role(self, request: Request, pk: int | None = None) -> Response:  # noqa: ARG002
        user = self.get_object()

        serializer = ChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = serializer.validated_data["role"]

        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return Response({"detail": "Role updated"})
