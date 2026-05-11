import pytest
from django.urls import reverse
from rest_framework import status

from product import constants as product_constants
from product.tests.factories import ProductAvailabilityFactory, ProductFactory
from user import constants as user_constants
from user.permissions import get_user_role_rank

PRODUCT_LIST_URL = reverse("product:product-list")

pytestmark = pytest.mark.django_db


def test_retrieve_product_list_endpoint_requires_authentication(api_client):
    response = api_client.get(PRODUCT_LIST_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "actor_fixture",
    (
        "super_user",
        "admin_user",
        "supervisor_user",
        "manager_user",
        "default_user",
    ),
)
def test_user_sees_only_allowed_regions_and_no_quantity_without_permission_except_for_superuser_in_product_list(
    auth_client,
    request,
    actor_fixture,
    region,
    grant_user_permissions,
):

    actor = request.getfixturevalue(actor_fixture)
    eu = region(product_constants.Regions.EU)
    us = region(product_constants.Regions.US)

    product_one, product_two = ProductFactory.create_batch(2)

    ProductAvailabilityFactory(product=product_one, region=eu)
    ProductAvailabilityFactory(product=product_two, region=us)

    grant_user_permissions(
        user=actor,
        region=eu,
        permissions=(user_constants.ProductPermissionType.VIEW_PRODUCT,),
    )

    response = auth_client(actor).get(PRODUCT_LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["code"] == str(product_one.code)
    if actor.is_superuser:
        assert response.json()["results"][0]["quantity"] == float(product_one.quantity)
    else:
        assert response.json()["results"][0]["quantity"] is None


@pytest.mark.parametrize(
    "actor_fixture",
    (
        "super_user",
        "admin_user",
        "supervisor_user",
        "manager_user",
        "default_user",
    ),
)
def test_user_sees_quantity_if_allowed_and_has_respective_rank_in_product_list(
    auth_client,
    request,
    actor_fixture,
    region,
    grant_user_permissions,
):

    actor = request.getfixturevalue(actor_fixture)
    eu = region(product_constants.Regions.EU)

    product_one, product_two = ProductFactory.create_batch(2)

    ProductAvailabilityFactory(product=product_one, region=eu)
    ProductAvailabilityFactory(product=product_two, region=eu)

    grant_user_permissions(
        user=actor,
        region=eu,
        permissions=(
            user_constants.ProductPermissionType.VIEW_PRODUCT,
            user_constants.ProductPermissionType.SEE_QUANTITY,
        ),
    )

    response = auth_client(actor).get(PRODUCT_LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 2

    if get_user_role_rank(actor) > user_constants.Ranks.DEFAULT_USER:
        assert response.json()["results"][0]["quantity"] == float(product_one.quantity)
        assert response.json()["results"][1]["quantity"] == float(product_two.quantity)

    else:
        assert response.json()["results"][0]["quantity"] is None
        assert response.json()["results"][1]["quantity"] is None
