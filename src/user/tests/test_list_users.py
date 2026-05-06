import pytest
from django.urls import reverse
from rest_framework import status

from user import constants
from user.tests.factories import UserFactory

USER_LIST_URL = reverse("user:user-list")

pytestmark = pytest.mark.django_db


def test_user_list_endpoint_requires_authentication(api_client):
    response = api_client.get(USER_LIST_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "user_fixture",
    (
        "supervisor_user",
        "manager_user",
        "default_user",
    ),
)
def test_not_admins_not_allowed_to_list_users(auth_client, request, user_fixture):
    user = request.getfixturevalue(user_fixture)

    response = auth_client(user).get(USER_LIST_URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    ("user_fixture", "num_of_returned_records"),
    (
        ("super_user", 4),
        ("admin_user", 3),
    ),
)
def test_admin_users_can_list_users_with_respective_role_ranks(
    user_fixture,
    request,
    auth_client,
    num_of_returned_records,
):
    user = request.getfixturevalue(user_fixture)

    UserFactory.create(is_superuser=True)
    UserFactory.create(role=constants.Roles.ADMIN)
    UserFactory.create()

    response = auth_client(user).get(USER_LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == num_of_returned_records
