import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture"),
    (
        ("super_user", "admin_user"),
        ("super_user", "supervisor_user"),
        ("super_user", "manager_user"),
        ("super_user", "default_user"),
        ("admin_user", "admin_user"),
        ("admin_user", "supervisor_user"),
        ("admin_user", "manager_user"),
        ("admin_user", "default_user"),
        ("supervisor_user", "supervisor_user"),
        ("manager_user", "manager_user"),
        ("default_user", "default_user"),
    ),
)
def test_admin_user_retrieve_self_or_another_user_with_permissions_success(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_retrieve_url = reverse("user:user-detail", kwargs={"pk": target.pk})

    response = auth_client(actor).get(user_retrieve_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "role": target.groups.first().name,
        "email": target.email,
        "first_name": target.first_name,
        "middle_name": target.middle_name,
        "last_name": target.last_name,
    }


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture", "expected_status_code"),
    (
        ("super_user", "super_user", status.HTTP_403_FORBIDDEN),
        ("super_user", "another_super_user", status.HTTP_403_FORBIDDEN),
        ("admin_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("admin_user", "another_admin_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("supervisor_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "another_supervisor_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "manager_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "default_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("manager_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "supervisor_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "another_manager_user", status.HTTP_403_FORBIDDEN),
        ("manager_user", "default_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("default_user", "admin_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "supervisor_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "manager_user", status.HTTP_403_FORBIDDEN),
        ("default_user", "another_default_user", status.HTTP_403_FORBIDDEN),
    ),
)
def test_retrieve_self_or_another_user_without_permission_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    expected_status_code,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_retrieve_url = reverse("user:user-detail", kwargs={"pk": target.pk})

    response = auth_client(actor).get(user_retrieve_url)

    assert response.status_code == expected_status_code
