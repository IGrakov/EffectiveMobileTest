import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from product.constants import Regions
from product.models import Product, ProductAvailability, Region
from product.tests.factories import ProductFactory
from user.constants import ProductPermissionType, Roles
from user.models import User
from user.tests.factories import UserFactory, UserProductPermissionFactory


class Command(BaseCommand):
    help = "Seed database with test data"

    def add_arguments(self, parser) -> None:  # noqa: ANN001
        parser.add_argument("--products", type=int, default=10)
        parser.add_argument("--users", type=int, default=2)
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:  # noqa: ANN002, ANN003, ARG002
        if options["flush"]:
            self.stdout.write("Flushing database...")
            ProductAvailability.objects.all().delete()
            Product.objects.all().delete()
            Region.objects.all().delete()
            User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating users..."))
        for role in Roles.choices:
            UserFactory.create_batch(size=options["users"], role=role)

        self.stdout.write(self.style.SUCCESS("Creating regions..."))
        regions = []
        for code, name in Regions.choices:
            region, _ = Region.objects.get_or_create(
                code=code,
                defaults={"name": name},
            )
            regions.append(region)

        self.stdout.write(self.style.SUCCESS("Creating products..."))
        products = ProductFactory.create_batch(size=options["products"])

        self.stdout.write(self.style.SUCCESS("Creating product availabilities..."))
        for product in products:
            selected_regions = random.sample(regions, k=random.randint(1, 3))  # noqa: S311

            for region in selected_regions:
                price = product.price_per_unit * Decimal(str(random.uniform(0.9, 1.1)))  # noqa: S311

                ProductAvailability.objects.create(
                    product=product,
                    region=region,
                    price_override=price,
                    is_active=True,
                )

        self.stdout.write(self.style.SUCCESS("Creating user product permissions..."))
        regions = list(Region.objects.all())

        for user in User.objects.all():
            allowed_regions = random.sample(
                regions,
                k=random.randint(0, len(regions)),  # noqa: S311
            )

            for region in allowed_regions:
                UserProductPermissionFactory(
                    user=user,
                    region=region,
                    permission=random.choice(ProductPermissionType.values),  # noqa: S311
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
