import pytest
from django.urls import reverse
from rest_framework import status

from user.tests.factories import UserProductPermissionFactory

pytestmark = pytest.mark.django_db


def test_retrieve_user_permission_endpoint_requires_authentication(api_client):
    user_permission_retrieve_url = reverse("user:user-product-permission-detail", kwargs={"pk": 1})
    response = api_client.get(user_permission_retrieve_url)

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
def test_retrieve_user_permission_success(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    permission = UserProductPermissionFactory(user=target)

    user_permission_retrieve_url = reverse("user:user-product-permission-detail", kwargs={"pk": permission.pk})
    response = auth_client(actor).get(user_permission_retrieve_url)

    assert response.status_code == status.HTTP_200_OK


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
def test_retrieve_user_permission_if_not_allowed_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    permission = UserProductPermissionFactory(user=target)

    user_permission_retrieve_url = reverse("user:user-product-permission-detail", kwargs={"pk": permission.pk})
    response = auth_client(actor).get(user_permission_retrieve_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
