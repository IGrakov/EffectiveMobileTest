from django.core.management.base import BaseCommand
from django.db import transaction

from product.models import Product
from product.tests.factories import ProductFactory


class Command(BaseCommand):
    help = "Seed product database with data"

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=10)
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing database...")
            Product.objects.all().delete()

        ProductFactory.create_batch(options["products"])

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
