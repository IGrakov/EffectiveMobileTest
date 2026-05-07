import random
import uuid

import factory

from product.models import Product, UnitType


class ProductFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating products.
    """

    class Meta:
        model = Product

    code = factory.LazyFunction(uuid.uuid4)

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=2)

    quantity = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
    )

    price_per_unit = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
    )

    unit_type = factory.LazyFunction(
        lambda: random.choice(UnitType.values)
    )
