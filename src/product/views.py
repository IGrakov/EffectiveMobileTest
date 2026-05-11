from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from product.models import ProductAvailability
from product.serializers import ProductAvailabilitySerializer
from user import constants as user_constants
from user.services.product_permission_service import ProductPermissionService


class ProductListView(generics.ListAPIView):
    """List products"""

    permission_service: ProductPermissionService
    serializer_class = ProductAvailabilitySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ProductAvailability.objects.none()

        user = self.request.user

        self.permission_service = ProductPermissionService(user)

        allowed_region_ids = self.permission_service.get_allowed_regions(
            user_constants.ProductPermissionType.VIEW_PRODUCT,
        )

        if not allowed_region_ids:
            return ProductAvailability.objects.none()

        return ProductAvailability.objects.select_related("product", "region").filter(
            is_active=True,
            region_id__in=allowed_region_ids,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["permission_service"] = self.permission_service
        return context
