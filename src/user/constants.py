from django.db import models


class Roles(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    DEFAULT = 'Default', 'Default'
    SUPERVISOR = 'Supervisor', 'Supervisor'
