# users/tests/test_profile.py

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from ..models import Profile, User


class TestProfile(TestCase):
    def setUp(self):
        # Define user credentials
        self.email = "test1234@gmail.com"
        self.password = "test1234"
        self.first_name = "test"
        self.last_name = "test"
        self.phone_number = "123456789"

        # Register user
        self.client.post(
            reverse("register"),
            {
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            }
        )

        self.user = User.objects.get(email=self.email)

    # Test if user can view their profile
    def test_profile_page(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(user=self.user)

        self.assertTrue(profile)

    # Test if user can add information
    def test_add_profile_information(self):
        user_information = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
        }

        response = self.client.post(
            reverse("edit-profile"),
            user_information,
        )

        self.assertEqual(response.status_code, 302)

        profile = Profile.objects.get(user=self.user)

        self.assertEqual(profile.first_name, self.first_name)
        self.assertEqual(profile.last_name, self.last_name)
        self.assertEqual(profile.phone_number, self.phone_number)

    # Test profile avatar
    def test_add_profile_avatar(self):
        image = Image.new("RGB", (100, 100), "white")

        image_file = BytesIO()
        image.save(image_file, format="JPEG")
        image_file.seek(0)

        avatar = SimpleUploadedFile(
            "test.jpg",
            image_file.read(),
            content_type="image/jpeg",
        )

        response = self.client.post(
            reverse("edit-profile"),
            {
                "avatar": avatar,
            },
        )

        self.assertEqual(response.status_code, 302)

        profile = Profile.objects.get(user=self.user)

        self.assertTrue(profile.avatar)
        self.assertTrue(profile.avatar.storage.exists(profile.avatar.name))
        self.assertTrue(profile.avatar.name.endswith(".jpg"))
        self.assertTrue(profile.avatar.name.startswith("avatars/"))