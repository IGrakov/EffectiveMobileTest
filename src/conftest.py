import random
import time

import pytest
from django.contrib.auth.models import Group
from django.core.cache import cache
from rest_framework.test import APIClient

from user import constants
from user.tests.factories import UserFactory

TEST_FIRST_NAME = "Test first name"
TEST_LAST_NAME = "Test last name"
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "test_pass123"


def pytest_collection_modifyitems(items):
    """Randomizes tests in order to prevent mutual dependencies."""

    # use current UNIX timestamp as seed
    seed = int(time.time())
    random.seed(seed)

    print(f"\npytest: randomizing tests order with seed = {seed}\n")  # noqa: T201

    random.shuffle(items)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    try:
        yield
    finally:
        cache.clear()


@pytest.fixture(autouse=True)
def fast_password_hashers(settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]


@pytest.fixture(autouse=True)
def create_roles(db):  # noqa: ARG001
    for role in constants.Roles:
        Group.objects.get_or_create(name=role)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def super_user():
    return UserFactory(first_name="superuser", last_name="superuser", is_superuser=True)


@pytest.fixture
def admin_user():
    return UserFactory(first_name="admin", last_name="admin", role=constants.Roles.ADMIN)


@pytest.fixture
def supervisor_user():
    return UserFactory(first_name="supervisor", last_name="supervisor", role=constants.Roles.SUPERVISOR)


@pytest.fixture
def manager_user():
    return UserFactory(first_name="manager", last_name="manager", role=constants.Roles.MANAGER)


@pytest.fixture
def default_user():
    return UserFactory(first_name="default", last_name="default", role=constants.Roles.DEFAULT)


@pytest.fixture
def auth_client(api_client):
    def _auth(user):
        api_client.force_authenticate(user=user)
        return api_client

    return _auth


@pytest.fixture
def login_user_payload():
    return {
        "email": "test_email",
        "password": "test_login_password",
    }


@pytest.fixture
def login_user(login_user_payload):
    return UserFactory(
        email=login_user_payload.get("email"),
        password=login_user_payload.get("password"),
    )


@pytest.fixture
def login_user_api_client(api_client, login_user):
    api_client.force_authenticate(user=login_user)
    return api_client


@pytest.fixture
def user_update_payload():
    return {
        "first_name": TEST_FIRST_NAME,
        "last_name": TEST_LAST_NAME,
        "password": TEST_PASSWORD,
    }


@pytest.fixture
def user_create_payload(user_update_payload):
    return {
        **user_update_payload,
        "email": TEST_EMAIL,
    }
