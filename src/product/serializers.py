from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            "code",
            "title",
            "description",
            "quantity",
            "price_per_unit",
            "unit_type",
        )
