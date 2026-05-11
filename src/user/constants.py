from django.db import models


class Roles(models.TextChoices):
    ADMIN = "Admin", "Admin"
    DEFAULT = "Default", "Default"
    MANAGER = "Manager", "Manager"
    SUPERVISOR = "Supervisor", "Supervisor"


class Ranks(models.IntegerChoices):
    INACTIVE_USER = -1
    SUPERUSER = 100
    ADMIN = 80
    SUPERVISOR = 50
    MANAGER = 30
    DEFAULT_USER = 0


class ProductPermissionType(models.TextChoices):
    VIEW_PRODUCT = "VIEW_PRODUCT"
    SEE_QUANTITY = "SEE_QUANTITY"
    EDIT_PRICE = "EDIT_PRICE"


PRODUCT_PERMISSION_MIN_RANK = {
    ProductPermissionType.VIEW_PRODUCT: Ranks.DEFAULT_USER,
    ProductPermissionType.SEE_QUANTITY: Ranks.MANAGER,
    ProductPermissionType.EDIT_PRICE: Ranks.SUPERVISOR,
}
