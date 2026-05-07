import pytest
from django.urls import reverse
from rest_framework import status

from product import constants as product_constants
from user import constants


def test_retrieve_user_permissions_endpoint_requires_authentication(api_client):
    retrieve_user_permissions_url = reverse("user:user-product-permissions", kwargs={"pk": 1})
    response = api_client.post(retrieve_user_permissions_url, {})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture"),
    (
        ("super_user", "super_user"),
        ("super_user", "another_super_user"),
        ("super_user", "admin_user"),
        ("super_user", "supervisor_user"),
        ("super_user", "manager_user"),
        ("super_user", "default_user"),
        ("admin_user", "supervisor_user"),
        ("admin_user", "manager_user"),
        ("admin_user", "default_user"),
    ),
)
def test_retrieve_user_permissions_success(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    region,
    user_product_permission,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    retrieve_user_permissions_url = reverse("user:user-product-permissions", kwargs={"pk": target.id})

    region = region(product_constants.Regions.EU)
    permission_one = user_product_permission(
        user=target,
        region=region,
        permission=constants.ProductPermissionType.VIEW_PRODUCT,
    )
    permission_two = user_product_permission(
        user=target,
        region=region,
        permission=constants.ProductPermissionType.EDIT_PRICE,
    )

    response = auth_client(actor).get(retrieve_user_permissions_url)

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "user": target.id,
        "permissions": [
            {
                "id": permission_two.id,
                "user": permission_two.user.id,
                "region": permission_two.region.code,
                "permission": permission_two.permission.value,
                "is_allowed": permission_two.is_allowed,
            },
            {
                "id": permission_one.id,
                "user": permission_one.user.id,
                "region": permission_one.region.code,
                "permission": permission_one.permission.value,
                "is_allowed": permission_one.is_allowed,
            },
        ],
    }


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture"),
    (
        ("admin_user", "super_user"),
        ("admin_user", "admin_user"),
        ("admin_user", "another_admin_user"),
        ("supervisor_user", "super_user"),
        ("supervisor_user", "admin_user"),
        ("supervisor_user", "supervisor_user"),
        ("supervisor_user", "another_supervisor_user"),
        ("supervisor_user", "manager_user"),
        ("supervisor_user", "default_user"),
        ("manager_user", "super_user"),
        ("manager_user", "admin_user"),
        ("manager_user", "supervisor_user"),
        ("manager_user", "manager_user"),
        ("manager_user", "another_manager_user"),
        ("manager_user", "default_user"),
        ("default_user", "super_user"),
        ("default_user", "admin_user"),
        ("default_user", "supervisor_user"),
        ("default_user", "manager_user"),
        ("default_user", "default_user"),
        ("default_user", "another_default_user"),
    ),
)
def test_retrieve_user_permissions_if_not_allowed_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    retrieve_user_permissions_url = reverse("user:user-product-permissions", kwargs={"pk": target.id})

    response = auth_client(actor).get(retrieve_user_permissions_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
