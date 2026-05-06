import jwt
import pytest
from django.conf import settings
from django.urls import reverse
from jwt import InvalidTokenError
from rest_framework import status

LOGIN_URL = reverse("user:login")

pytestmark = pytest.mark.django_db


def test_login_success(api_client, login_user, login_user_payload):  # noqa: ARG001
    response = api_client.post(
        LOGIN_URL,
        {
            "email": login_user_payload.get("email"),
            "password": login_user_payload.get("password"),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "access" in data
    assert "refresh" in data

    # Check that tokens are valid
    try:
        jwt.decode(data["access"], settings.SECRET_KEY, algorithms=["HS256"])
        jwt.decode(data["refresh"], settings.SECRET_KEY, algorithms=["HS256"])
    except InvalidTokenError as exception:
        pytest.fail(f"Token validation failed: {exception}")


def test_login_wrong_password(api_client, login_user, login_user_payload):  # noqa: ARG001
    response = api_client.post(
        LOGIN_URL,
        {
            "email": login_user_payload.get("email"),
            "password": "wrong_password",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_wrong_email_or_non_existing_user(
    api_client,
    login_user,  # noqa: ARG001
    login_user_payload,
):
    response = api_client.post(
        LOGIN_URL,
        {
            "email": "wrong_email",
            "password": login_user_payload.get("password"),
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_missing_password(api_client, login_user, login_user_payload):  # noqa: ARG001
    response = api_client.post(
        LOGIN_URL,
        {"email": login_user_payload.get("email")},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"password": ["This field is required."]}


def test_login_missing_email(api_client, login_user, login_user_payload):  # noqa: ARG001
    response = api_client.post(
        LOGIN_URL,
        {"password": login_user_payload.get("password")},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"email": ["This field is required."]}
