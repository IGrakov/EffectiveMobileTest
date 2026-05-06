import pytest
from django.urls import reverse
from rest_framework import status

from user import constants

pytestmark = pytest.mark.django_db


def test_update_role_endpoint_requires_authentication(api_client):
    user_update_role_url = reverse("user:user-change-role", kwargs={"pk": 1})
    response = api_client.post(user_update_role_url, {})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture", "new_role"),
    (
        ("super_user", "admin_user", constants.Roles.DEFAULT),
        ("super_user", "admin_user", constants.Roles.MANAGER),
        ("super_user", "admin_user", constants.Roles.SUPERVISOR),
        ("super_user", "supervisor_user", constants.Roles.ADMIN),
        ("super_user", "supervisor_user", constants.Roles.MANAGER),
        ("super_user", "supervisor_user", constants.Roles.DEFAULT),
        ("super_user", "manager_user", constants.Roles.ADMIN),
        ("super_user", "manager_user", constants.Roles.SUPERVISOR),
        ("super_user", "manager_user", constants.Roles.DEFAULT),
        ("super_user", "default_user", constants.Roles.ADMIN),
        ("super_user", "default_user", constants.Roles.SUPERVISOR),
        ("super_user", "default_user", constants.Roles.MANAGER),
        ("admin_user", "supervisor_user", constants.Roles.MANAGER),
        ("admin_user", "supervisor_user", constants.Roles.DEFAULT),
        ("admin_user", "manager_user", constants.Roles.SUPERVISOR),
        ("admin_user", "manager_user", constants.Roles.DEFAULT),
        ("admin_user", "default_user", constants.Roles.SUPERVISOR),
        ("admin_user", "default_user", constants.Roles.MANAGER),
    ),
)
def test_admin_user_update_role_of_another_user_with_permissions_except_admin_role_success(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    new_role,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_update_role_url = reverse("user:user-change-role", kwargs={"pk": target.pk})

    response = auth_client(actor).patch(user_update_role_url, {"role": new_role}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "detail": "Role updated",
    }

    target.refresh_from_db()

    assert target.groups.first().name == new_role


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture", "new_role"),
    (
        ("admin_user", "supervisor_user", constants.Roles.ADMIN),
        ("admin_user", "manager_user", constants.Roles.ADMIN),
        ("admin_user", "default_user", constants.Roles.ADMIN),
    ),
)
def test_admin_user_being_not_superuser_cannot_change_role_to_admin_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    new_role,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_update_role_url = reverse("user:user-change-role", kwargs={"pk": target.pk})

    response = auth_client(actor).patch(user_update_role_url, {"role": new_role}, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Only superuser can assign admin role",
    }


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture", "expected_status_code"),
    (
        ("super_user", "super_user", status.HTTP_403_FORBIDDEN),
        ("super_user", "another_super_user", status.HTTP_403_FORBIDDEN),
        ("admin_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("admin_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("admin_user", "another_admin_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("supervisor_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "supervisor_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "another_supervisor_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "manager_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "default_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("manager_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "supervisor_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "manager_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "another_manager_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "default_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("default_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "supervisor_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "manager_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "default_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "another_default_user", status.HTTP_403_FORBIDDEN),
    ),
)
def test_update_role_without_permission_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    expected_status_code,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_update_role_url = reverse("user:user-change-role", kwargs={"pk": target.pk})

    response = auth_client(actor).patch(user_update_role_url, {}, format="json")

    assert response.status_code == expected_status_code
