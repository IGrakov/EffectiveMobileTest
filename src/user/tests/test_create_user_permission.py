import pytest
from django.urls import reverse
from rest_framework import status

from product import constants as product_constants
from user import constants

USER_PERMISSION_CREATE_URL = reverse("user:user-product-permission-list")

pytestmark = pytest.mark.django_db


def test_create_user_permission_endpoint_requires_authentication(api_client):
    response = api_client.post(USER_PERMISSION_CREATE_URL, {})

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
def test_create_user_permission_success(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    region,
):
    region = region(product_constants.Regions.EU)
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)

    payload = {
        "user": target.id,
        "region": region.id,
        "permission": constants.ProductPermissionType.VIEW_PRODUCT,
        "is_allowed": True,
    }

    response = auth_client(actor).post(USER_PERMISSION_CREATE_URL, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED


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
def test_create_user_permission_if_not_allowed_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    region,
):
    region = region(product_constants.Regions.EU)
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)

    payload = {
        "user": target.id,
        "region": region.id,
        "permission": constants.ProductPermissionType.VIEW_PRODUCT,
        "is_allowed": True,
    }

    response = auth_client(actor).post(USER_PERMISSION_CREATE_URL, payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN
