import pytest
from django.urls import reverse
from rest_framework import status

LOGIN_URL = reverse("user:login")
LOGOUT_URL = reverse("user:logout")
REFRESH_TOKEN_URL = reverse("user:refresh-token")

pytestmark = pytest.mark.django_db


def test_logout_endpoint_requires_authentications(api_client):
    response = api_client.post(LOGOUT_URL, {"refresh": "12345"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_user_success(api_client, login_user, login_user_payload):
    response = api_client.post(
        LOGIN_URL,
        {
            "email": login_user_payload.get("email"),
            "password": login_user_payload.get("password"),
        },
    )

    refresh_token = response.json()["refresh"]
    api_client.force_authenticate(user=login_user)

    response = api_client.post(LOGOUT_URL, {"refresh": refresh_token})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Successfully logged out"}

    response = api_client.post(REFRESH_TOKEN_URL, {"refresh": refresh_token})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token is blacklisted"


def test_logout_wrong_refresh_token(auth_client, login_user):
    response = auth_client(login_user).post(LOGOUT_URL, {"refresh": "wrong_token"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"refresh": "Invalid or expired refresh token"}
