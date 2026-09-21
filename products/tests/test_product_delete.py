# products/tests/test_product_delete.py

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from ..models import Product, Category, ProductImage

class TestProductDelete(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Define product details
        cls.title = "Test Title"
        cls.description = "Test description"
        cls.price = 1000
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

        # Create product
        cls.product = Product.objects.create(
            title=cls.title,
            description=cls.description,
            price=cls.price,
            category=cls.category,
        )

        # Adding product image
        cls.product_image = ProductImage.objects.create(
            product=cls.product,
            image=cls.image,
        )

    # Test with deleting a product
    def test_product_delete(self):
        # Try to delete product
        response = self.client.post(
            reverse("products:product-delete", kwargs={"slug": self.product.slug}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
        self.assertFalse(ProductImage.objects.filter(product=self.product).exists())

    # Test with a non-existing slug
    def test_product_delete_with_absent_slug(self):
        # Try to delete product
        response = self.client.post(
            reverse("products:product-delete", kwargs={"slug": "wrong-slug"}),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Product.objects.filter(title=self.title).exists())
        self.assertTrue(ProductImage.objects.filter(product=self.product).exists())

