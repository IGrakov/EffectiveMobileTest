import uuid

from django.db import models

from core.models import TimeStampMixin


class UnitType(models.TextChoices):
    KG = "KG", "Kilogram"
    TON = "TON", "Ton"
    LITRE = "LITRE", "Litre"
    PIECE = "PIECE", "Piece"
    BOTTLE = "BOTTLE", "Bottle"
    PACK = "PACK", "Pack"
    SET = "SET", "Set"
    BAG = "BAG", "Bag"
    CAN = "CAN", "Can"
    BOX = "BOX", "Box"
    CARTON = "CARTON", "Carton"
    METER = "METER", "Meter"
    SQUARE_METER = "SQUARE_METER", "Square Meter"
    CUBIC_METER = "CUBIC_METER", "Cubic Meter"


class Product(TimeStampMixin):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(
        max_length=20,
        choices=UnitType.choices,
    )


class Region(TimeStampMixin):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)


class ProductAvailability(TimeStampMixin):
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("product", "region"),
                name="unique_product_region",
            ),
        )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="availabilities",
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="product_availabilities",
    )

    is_active = models.BooleanField(default=True)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
