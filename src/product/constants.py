from django.db import models


class Regions(models.TextChoices):
    US = "US", "United States"
    EU = "EU", "European Union"
    APAC = "APAC", "Asia Pacific"
    CHINA = "CH", "China"
    MIDDLE_EAST = "ME", "Middle East"
    LATIN_AMERICA = "LA", "Latin America"
    AFRICA = "AF", "Africa"
