# users/tests/test_login.py

from django.test import TestCase
from django.urls import reverse


class TestLogin(TestCase):
    def setUp(self):
        self.password = "test1234"
        self.email = "test1234@gmail.com"

        self.client.post(
            reverse("register"),
            {
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            }
        )

        self.client.logout()

    # Test if user can login
    def test_user_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.email,
                "password": self.password,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # Test if an error occurs when the password is wrong
    def test_invalid_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.email,
                "password": "wrong-password",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # Test if an error occurs when the email is wrong
    def test_invalid_email(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "unknown@gmail.com",
                "password": self.password,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)