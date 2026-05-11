from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from user.models import User, UserProductPermission
from user.permissions import CanManagePermissions
from user.serializers import UserProductPermissionSerializer
from user.serializers.user_product_permission_serializer import (
    UserPermissionsResponseSerializer,
    UserProductPermissionItemSerializer,
)


@extend_schema(
    tags=["product permissions"],
)
class UserProductPermissionViewSet(ModelViewSet):
    serializer_class = UserProductPermissionSerializer
    queryset = UserProductPermission.objects.select_related(
        "user",
        "region",
    )
    permission_classes = (CanManagePermissions,)

    def perform_create(self, serializer: BaseSerializer) -> None:
        target_user = serializer.validated_data["user"]

        self.check_object_permissions(
            self.request,
            target_user,
        )

        serializer.save()


class UserProductPermissionsView(GenericAPIView):
    serializer_class = UserProductPermissionItemSerializer
    queryset = User.objects.prefetch_related("permissions__region")
    permission_classes = (CanManagePermissions,)

    @extend_schema(
        tags=["product permissions"],
        responses=UserPermissionsResponseSerializer,
    )
    def get(self, request: Request, pk: int) -> Response:  # noqa: ARG002
        user = self.get_object()

        permissions = UserProductPermission.objects.filter(user=user).select_related("region")

        serializer = self.get_serializer_class()(
            permissions,
            many=True,
        )

        response = {
            "user": user.id,
            "permissions": serializer.data,
        }

        return Response(response)
