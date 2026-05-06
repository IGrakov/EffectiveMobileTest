import jwt
import pytest
from django.conf import settings
from django.urls import reverse
from jwt import InvalidTokenError
from rest_framework import status

LOGIN_URL = reverse("user:login")
REFRESH_TOKEN_URL = reverse("user:refresh-token")

pytestmark = pytest.mark.django_db


def test_refresh_token_endpoint_requires_authentications(api_client):
    response = api_client.post(REFRESH_TOKEN_URL, {"refresh": "12345"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token_success(api_client, login_user, login_user_payload):
    response = api_client.post(
        LOGIN_URL,
        {
            "email": login_user_payload.get("email"),
            "password": login_user_payload.get("password"),
        },
    )

    token = response.json()["refresh"]
    api_client.force_authenticate(user=login_user)

    response = api_client.post(REFRESH_TOKEN_URL, {"refresh": token})

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


def test_refresh_token_wrong_token(api_client, login_user):
    api_client.force_authenticate(user=login_user)

    response = api_client.post(REFRESH_TOKEN_URL, {"refresh": "wrong_token"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token is invalid"
