# users/tests/test_user_creation.py

from django.test import TestCase
from ..models import User


class TestUserCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test123@gmail.com", password="test1234")

    # Test if user created
    def test_user_created(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, "test123@gmail.com")

    # Test if password is hashed
    def test_password_is_hashed(self):
        self.assertNotEqual(self.user.password, "test1234")

        self.assertTrue(self.user.check_password("test1234"))