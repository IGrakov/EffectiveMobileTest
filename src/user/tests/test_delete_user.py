import pytest
from django.urls import reverse
from rest_framework import status

from user.models import User

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
def test_admin_user_delete_self_or_another_user_with_permissions_success(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_delete_url = reverse("user:user-detail", kwargs={"pk": target.pk})

    response = auth_client(actor).delete(user_delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    target.refresh_from_db()

    # Check for soft delete
    assert not target.is_active
    assert User.objects.filter(pk=target.pk).exists()


@pytest.mark.parametrize(
    ("actor_fixture", "target_fixture", "expected_status_code"),
    (
        ("super_user", "super_user", status.HTTP_403_FORBIDDEN),
        ("super_user", "another_super_user", status.HTTP_403_FORBIDDEN),
        ("admin_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("admin_user", "another_admin_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "super_user", status.HTTP_404_NOT_FOUND),
        ("supervisor_user", "another_supervisor_user", status.HTTP_403_FORBIDDEN),
        ("supervisor_user", "admin_user", status.HTTP_403_FORBIDDEN),
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
def test_delete_self_or_another_user_without_permission_failure(
    auth_client,
    request,
    actor_fixture,
    target_fixture,
    expected_status_code,
):
    actor = request.getfixturevalue(actor_fixture)
    target = request.getfixturevalue(target_fixture)
    user_delete_url = reverse("user:user-detail", kwargs={"pk": target.pk})

    response = auth_client(actor).delete(user_delete_url)

    assert response.status_code == expected_status_code
