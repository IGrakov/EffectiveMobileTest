import random

from django.core.management.base import BaseCommand
from django.db import transaction

from product.constants import Regions
from product.models import Product, ProductAvailability, Region
from product.tests.factories import ProductFactory


class Command(BaseCommand):
    help = "Seed product database with data"

    def add_arguments(self, parser) -> None:  # noqa: ANN001
        parser.add_argument("--products", type=int, default=10)
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

        regions = []
        for code, name in Regions.choices:
            region, _ = Region.objects.get_or_create(
                code=code,
                defaults={"name": name},
            )
            regions.append(region)

        products = ProductFactory.create_batch(options["products"])

        for product in products:
            selected_regions = random.sample(regions, k=random.randint(1, 3))  # noqa: S311

            for region in selected_regions:
                ProductAvailability.objects.create(
                    product=product,
                    region=region,
                    is_active=True,
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
