from typing import ClassVar, Iterable

from django.db.models import QuerySet
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.permissions import CanManageUser, IsAdmin
from user.serializers import (
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
    }

    def get_serializer_class(self) -> type[BaseSerializer]:
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_permissions(self) -> Iterable[BasePermission]:
        if self.action == "create":
            return (AllowAny(),)

        if self.action == "list":
            return (IsAdmin(),)

        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
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
