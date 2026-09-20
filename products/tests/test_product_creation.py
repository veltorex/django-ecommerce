# products/tests/test_product_creation.py

from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from PIL import Image

from ..models import Product, ProductImage, Category


class TestProductCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Define product details
        cls.title = "Test Product"
        cls.description = "Test description"
        cls.price = 600

        # Create test category
        cls.category = Category.objects.create(
            name="Test Category"
        )

    def setUp(self):
        # Create a test image in memory
        product_image = Image.new(
            "RGB",
            (100, 100),
            "white"
        )

        # Save the image to memory
        image_file = BytesIO()
        product_image.save(
            image_file,
            format="JPEG"
        )
        image_file.seek(0)

        # Convert the image into an uploaded file
        self.image = SimpleUploadedFile(
            "test.jpg",
            image_file.read(),
            content_type="image/jpeg",
        )

    # Test if a product can be created
    def test_product_create(self):
        # Submit the product creation form
        response = self.client.post(
            reverse("products:product-create"),
            {
                # Product form
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "category": self.category.pk,

                # Product image formset management form
                "images-TOTAL_FORMS": "1",
                "images-INITIAL_FORMS": "0",
                "images-MIN_NUM_FORMS": "0",
                "images-MAX_NUM_FORMS": "1000",

                # Product image
                "images-0-image": self.image,
            },
        )

        # Check the response status
        self.assertEqual(response.status_code, 302)

        # Check that the product was created
        product = Product.objects.get(
            title=self.title
        )

        # Check product fields
        self.assertEqual(product.description, self.description)
        self.assertEqual(product.price, self.price)
        self.assertEqual(product.category, self.category)
        self.assertTrue(
            ProductImage.objects.filter(
                product=product
            ).exists()
        )

        # Check that a product image was created
        self.assertTrue(
            ProductImage.objects.filter(
                product=product
            ).exists()
        )

