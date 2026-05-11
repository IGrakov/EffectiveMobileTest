from decimal import Decimal

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from product.models import ProductAvailability


class ProductAvailabilitySerializer(serializers.ModelSerializer):
    code = serializers.UUIDField(source="product.code")
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    unit_type = serializers.CharField(source="product.unit_type")

    quantity = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductAvailability

        fields = (
            "code",
            "title",
            "description",
            "quantity",
            "price",
            "unit_type",
        )

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_quantity(self, obj: ProductAvailability) -> Decimal | None:
        service = self.context.get("permission_service")

        if service and service.can_see_quantity(obj.region_id):
            return obj.product.quantity

        return None

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_price(self, obj: ProductAvailability) -> Decimal | None:
        return obj.price_override or obj.product.price_per_unit
