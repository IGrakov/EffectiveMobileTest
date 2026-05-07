from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import User, UserProductPermission
from user.permissions import CanManagePermissions, IsAdmin
from user.serializers import UserProductPermissionSerializer
from user.serializers.user_product_permission_serializer import (
    UserPermissionsResponseSerializer,
    UserProductPermissionItemSerializer,
)


class UserProductPermissionViewSet(ModelViewSet):
    queryset = UserProductPermission.objects.select_related(
        "user",
        "region",
    )
    serializer_class = UserProductPermissionSerializer
    permission_classes = (IsAdmin,)


class UserProductPermissionsView(GenericAPIView):
    serializer_class = UserProductPermissionItemSerializer
    queryset = User.objects.prefetch_related("permissions__region")
    permission_classes = (CanManagePermissions,)

    @extend_schema(
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
