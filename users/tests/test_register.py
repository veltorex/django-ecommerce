# users/tests/test_register.py

from django.test import TestCase
from django.urls import reverse
from ..models import User, Profile


class TestRegister(TestCase):
    def setUp(self):
        self.email = "test1234@gmail.com"
        self.password = "test1234"

    # Test if user can register
    def test_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("products:product-list"))
        self.assertTrue(User.objects.filter(email=self.email).exists())


    # Test if user profile is created
    def test_user_profile_created(self):
        self.client.post(
            reverse("register"),
            {
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
        )

        user = User.objects.get(email=self.email)

        self.assertTrue(
            Profile.objects.filter(user=user).exists()
        )