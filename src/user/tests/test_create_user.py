import pytest
from django.urls import reverse
from rest_framework import status

from user import constants
from user.models import User

USER_CREATE_URL = reverse("user:user-list")

pytestmark = pytest.mark.django_db


def test_superuser_assigned_admin_role_by_default(user_create_payload):
    user_create_payload.pop("first_name")
    user_create_payload.pop("middle_name")
    user_create_payload.pop("last_name")
    user_create_payload.pop("password_repeated")
    user = User.objects.create_superuser(**user_create_payload)

    assert user.groups.filter(name=constants.Roles.ADMIN).exists()


def test_user_create_success(
    api_client,
    user_create_payload,
):
    response = api_client.post(USER_CREATE_URL, user_create_payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        "email": user_create_payload["email"],
        "first_name": user_create_payload["first_name"],
        "middle_name": user_create_payload["middle_name"],
        "last_name": user_create_payload["last_name"],
    }

    user = User.objects.get(email=user_create_payload["email"])

    assert response.json() == {
        "email": user.email,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
    }

    assert user.check_password(user_create_payload["password"])
    assert user.groups.first().name == constants.Roles.DEFAULT
