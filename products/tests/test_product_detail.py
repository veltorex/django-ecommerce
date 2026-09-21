# products/tests/test_product_detail.py

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from ..models import Product, ProductImage, Category


class ProductDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Define product details
        cls.title = "Test Product"
        cls.description = "Test description"
        cls.price = 1000

        # Create a test category
        cls.category = Category.objects.create(
            name="Test Category"
        )

        # Create a test image in memory
        product_image = Image.new(
            "RGB",
            (100, 100),
            "white",
        )

        image_file = BytesIO()

        product_image.save(
            image_file,
            format="JPEG",
        )

        image_file.seek(0)

        # Convert the image into an uploaded file
        cls.image = SimpleUploadedFile(
            "test.jpg",
            image_file.read(),
            content_type="image/jpeg",
        )

        # Create the product
        cls.product = Product.objects.create(
            title=cls.title,
            description=cls.description,
            price=cls.price,
            category=cls.category,
        )

        # Add an image to the product
        cls.product_image = ProductImage.objects.create(
            product=cls.product,
            image=cls.image,
        )

    # Test that the product detail page loads successfully
    def test_product_detail(self):
        response = self.client.get(
            reverse(
                "products:product-detail",
                kwargs={"slug": self.product.slug},
            )
        )

        # The page should load successfully
        self.assertEqual(response.status_code, 200)

        # The correct product should be passed to the template
        self.assertEqual(
            response.context["product"],
            self.product,
        )

    # Test that the product information is displayed
    def test_product_detail_content(self):
        response = self.client.get(
            reverse(
                "products:product-detail",
                kwargs={"slug": self.product.slug},
            )
        )

        # Check that important product information is displayed
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.description)
        self.assertContains(response, str(self.product.price))
        self.assertContains(response, self.product.category.name)

    # Test that a non-existing product returns 404
    def test_product_detail_with_absent_slug(self):
        response = self.client.get(
            reverse(
                "products:product-detail",
                kwargs={"slug": "does-not-exist"},
            )
        )

        self.assertEqual(response.status_code, 404)

    # Test that the product has an image
    def test_product_detail_image(self):
        response = self.client.get(
            reverse(
                "products:product-detail",
                kwargs={"slug": self.product.slug},
            )
        )

        # The product should have at least one image
        self.assertTrue(
            response.context["product"].images.exists()
        )