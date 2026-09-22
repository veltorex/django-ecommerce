# users/tests/test_password_change.py

from django.test import TestCase
from django.urls import reverse
from ..models import User


class TestChangePassword(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Define user credentials
        cls.email = "test1234@gmail.com"
        cls.password = "test1234"

        # Create test user
        cls.user = User.objects.create_user(
            email=cls.email,
            password=cls.password
        )

    # Test successful password change
    def test_password_change(self):
        # Login user directly
        self.client.force_login(self.user)

        # Define the new password
        new_password = "test1234test1234"

        # Submit password change form
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": self.password,
                "new_password1": new_password,
                "new_password2": new_password,
            }
        )

        # PasswordChangeView redirects after a successful password change
        self.assertEqual(response.status_code, 302)

        # Reload user from database
        self.user.refresh_from_db()

        # Check that the new password works
        self.assertTrue(self.user.check_password(new_password))

        # Check that the old password no longer works
        self.assertFalse(self.user.check_password(self.password))

    # Test password change with incorrect old password
    def test_password_change_with_wrong_password(self):
        # Login user directly
        self.client.force_login(self.user)

        # Submit password change form with an incorrect old password
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": "wrong-password1234",
                "new_password1": "new-password1234",
                "new_password2": "new-password1234",
            }
        )

        # Form validation should fail
        self.assertEqual(response.status_code, 200)

        # Reload user from database
        self.user.refresh_from_db()

        # Check that the password was not changed
        self.assertTrue(self.user.check_password(self.password))

    # Test password change with a short password
    def test_password_change_with_short_password(self):
        # Login user directly
        self.client.force_login(self.user)

        # Submit a password shorter than Django's minimum length
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": self.password,
                "new_password1": "foo234",
                "new_password2": "foo234",
            }
        )

        # Form validation should fail
        self.assertEqual(response.status_code, 200)

        # Reload user from database
        self.user.refresh_from_db()

        # Check that the password was not changed
        self.assertTrue(self.user.check_password(self.password))

    # Test password change with mismatched passwords
    def test_password_change_with_mismatched_passwords(self):
        # Login user directly
        self.client.force_login(self.user)

        # Submit two different new passwords
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": self.password,
                "new_password1": "new-password1234",
                "new_password2": "different-password1234",
            }
        )

        # Form validation should fail because the passwords do not match
        self.assertEqual(response.status_code, 200)

        # Reload user from database
        self.user.refresh_from_db()

        # Check that the password was not changed
        self.assertTrue(self.user.check_password(self.password))