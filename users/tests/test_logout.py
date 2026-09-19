# users/tests/test_logout.py

from django.test import TestCase
from django.urls import reverse
from ..models import User


class TestLogout(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Define user credentials
        cls.email = "test1234@gmail.com"
        cls.password = "test1234"

        # Create user
        cls.user = User.objects.create_user(
            email=cls.email,
            password=cls.password
        )

    def setUp(self):
        # Login user
        self.client.login(
            email=self.email,
            password=self.password
        )

    # Test if user can logout
    def test_logout(self):
        response = self.client.post(reverse("logout"))

        self.assertRedirects(
            response,
            reverse("products:product-list")
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)