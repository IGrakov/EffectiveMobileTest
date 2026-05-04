from django.test import TestCase
from django.urls import reverse


class HealthTest(TestCase):
    def test_status_code(self):
        """
        Always returns 200OK
        """
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
