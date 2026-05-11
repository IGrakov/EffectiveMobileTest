from collections import defaultdict

from user.constants import PRODUCT_PERMISSION_MIN_RANK, ProductPermissionType, Ranks
from user.models import User, UserProductPermission
from user.permissions import get_user_role_rank


class ProductPermissionService:
    def __init__(self, user: User) -> None:
        self.user = user

        permissions_map = defaultdict(set)

        qs = UserProductPermission.objects.filter(
            user=user,
            is_allowed=True,
        ).values_list("region_id", "permission")

        for region_id, permission in qs:
            permissions_map[region_id].add(permission)

        self.permissions = dict(permissions_map)

    def has_permission(self, region_id: int, permission_type: str) -> bool:
        if self.user.is_superuser:
            return True

        if permission_type not in self.permissions.get(region_id, set()):
            return False

        required_rank = PRODUCT_PERMISSION_MIN_RANK.get(permission_type, Ranks.DEFAULT_USER)
        return get_user_role_rank(self.user) >= required_rank

    def can_view_product(self, region_id: int) -> bool:
        return self.has_permission(
            region_id,
            ProductPermissionType.VIEW_PRODUCT,
        )

    def can_see_quantity(self, region_id: int) -> bool:
        return self.has_permission(
            region_id,
            ProductPermissionType.SEE_QUANTITY,
        )

    def can_edit_price(self, region_id: int) -> bool:
        return self.has_permission(
            region_id,
            ProductPermissionType.EDIT_PRICE,
        )

    def get_allowed_regions(self, permission_type: str) -> list[str]:
        return [region_id for region_id, perms in self.permissions.items() if permission_type in perms]
