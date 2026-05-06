import pytest
from django.urls import reverse
from rest_framework import status

CHANGE_PASSWORD_URL = reverse("user:change-password")
NEW_PASSWORD = "new_password"

pytestmark = pytest.mark.django_db


def test_change_password_endpoint_requires_authentication(api_client):
    response = api_client.post(CHANGE_PASSWORD_URL, {})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password_success(auth_client, login_user, login_user_payload):
    response = auth_client(login_user).post(
        CHANGE_PASSWORD_URL,
        {
            "old_password": login_user_payload["password"],
            "new_password": NEW_PASSWORD,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Password updated successfully"}

    login_user.refresh_from_db()
    assert login_user.check_password(NEW_PASSWORD)


def test_change_password_wrong_old_password(auth_client, login_user):
    response = auth_client(login_user).post(
        CHANGE_PASSWORD_URL,
        {
            "old_password": "wrong_password",
            "new_password": NEW_PASSWORD,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"old_password": "Invalid password"}
