import pytest
from django.urls import reverse
from rest_framework import status

CHANGE_EMAIL_URL = reverse("user:change-email")
NEW_EMAIL = "new_email@test.com"

pytestmark = pytest.mark.django_db


def test_change_email_success(auth_client, login_user, login_user_payload):
    response = auth_client(login_user).post(
        CHANGE_EMAIL_URL,
        {
            "email": NEW_EMAIL,
            "password": login_user_payload.get("password"),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Email updated successfully"}

    login_user.refresh_from_db()
    assert login_user.email == NEW_EMAIL


def test_change_email_wrong_password(auth_client, login_user):
    response = auth_client(login_user).post(
        CHANGE_EMAIL_URL,
        {
            "email": NEW_EMAIL,
            "password": "wrong_password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"password": "Invalid password"}


def test_change_email_already_exists(auth_client, login_user, login_user_payload, default_user):
    response = auth_client(login_user).post(
        CHANGE_EMAIL_URL,
        {
            "email": default_user.email,
            "password": login_user_payload.get("password"),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"email": ["Email already in use"]}
