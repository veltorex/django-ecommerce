# users/tests/test_password_reset.py

from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
import re
from ..models import User


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
class TestPasswordReset(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test1234@gmail.com",
            password="test1234",
        )

    # Test password reset flow
    def test_password_reset(self):
        response = self.client.post(
            reverse("password_reset"),
            {
                "email": self.user.email
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("password_reset_done"),
        )

        # Test password reset mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.user.email)
        self.assertTrue(mail.outbox[0].body)

        # Test reset URL
        match = re.search(
            r"http://testserver/accounts/reset/\S+",
            mail.outbox[0].body,
        )

        self.assertIsNotNone(match)

        reset_url = match.group(0)

        # Open reset URL
        response = self.client.get(reset_url)

        self.assertEqual(response.status_code, 302)

        reset_password_url = response.url

        # Set new password
        response = self.client.post(
            reset_password_url,
            {
                "new_password1": "X7!qP9@vL2#k",
                "new_password2": "X7!qP9@vL2#k",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("password_reset_complete"),
        )

        # Test password was changed
        self.user.refresh_from_db()
        self.assertTrue(
            self.user.check_password("X7!qP9@vL2#k")
        )

    # Test with invalid email
    def test_password_reset_with_invalid_email(self):
        response = self.client.post(
            reverse("password_reset"),
            {
                "email": "fake1234@gmail.com",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)