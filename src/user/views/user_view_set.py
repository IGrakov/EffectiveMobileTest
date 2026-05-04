from typing import ClassVar, Iterable

from django.db.models import Prefetch, prefetch_related_objects
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import BasePermission
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from user.models import User
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
    lookup_field = "username"

    def get_object(self) -> User:
        user = self.request.user
        if self.kwargs.get("username") == user.username:
            prefetch_related_objects(
                (user,),
                Prefetch("merchant", queryset=Merchant.objects.all()),
            )
            return user
        return super().get_object()

    # def get_permissions(self) -> Iterable[BasePermission]:
    #     if self.action == "create":
    #         return (IsAdmin(),)
    #     return (IsSelfOrAdmin(),)

    def perform_create(self, serializer: BaseSerializer) -> None:
        data = serializer.validated_data.copy()
        User.objects.create_user(
            merchant_id=data.pop("merchant").id,
            **data,
        )
