# products/tests/test_product_update.py

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from io import BytesIO
from ..models import Category, Product, ProductImage


class ProductUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Define common product details
        cls.title = "Test Product"
        cls.description = "Test description"
        cls.price = 600

        # Create categories for the product
        cls.category = Category.objects.create(
            name="Test Category"
        )

        cls.new_category = Category.objects.create(
            name="Test Category2"
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
            slug="test-product",
            description=cls.description,
            price=cls.price,
            category=cls.category,
        )

        # Add an image to the product
        ProductImage.objects.create(
            product=cls.product,
            image=cls.image,
        )

    # Test successful product update
    def test_product_update(self):
        response = self.client.post(
            reverse(
                "products:product-update",
                kwargs={"slug": self.product.slug},
            ),
            {
                "title": "Test Product2",
                "description": "New Description",
                "price": 234,
                "category": self.new_category.pk,
            },
        )

        # Successful form submission should redirect
        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()

        # Check that the product was actually updated
        self.assertEqual(self.product.title, "Test Product2")
        self.assertEqual(self.product.description, "New Description")
        self.assertEqual(self.product.price, 234)
        self.assertEqual(self.product.category, self.new_category)

    # Test product update with an invalid price
    def test_product_update_with_invalid_price(self):
        old_price = self.product.price

        response = self.client.post(
            reverse(
                "products:product-update",
                kwargs={"slug": self.product.slug},
            ),
            {
                "title": self.title,
                "description": self.description,
                "price": "invalid-price",
                "category": self.category.pk,
            },
        )

        # Invalid form data should render the form again
        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()

        # The invalid update must not change the existing price
        self.assertEqual(self.product.price, old_price)

    # Test product update with an invalid category
    def test_product_update_with_invalid_category(self):
        old_category = self.product.category

        response = self.client.post(
            reverse(
                "products:product-update",
                kwargs={"slug": self.product.slug},
            ),
            {
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "category": "invalid-category",
            },
        )

        # Invalid form data should render the form again
        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()

        # The invalid update must not change the existing category
        self.assertEqual(self.product.category, old_category)

    # Test product update with an empty title
    def test_product_update_with_empty_title(self):
        response = self.client.post(
            reverse(
                "products:product-update",
                kwargs={"slug": self.product.slug},
            ),
            {
                "title": "",
                "description": self.description,
                "price": self.price,
                "category": self.category.pk,
            },
        )

        # Empty title should make the form invalid
        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()

        # Existing title should remain unchanged
        self.assertEqual(self.product.title, self.title)
        
    # Test updating a product with a non-existing slug
    def test_product_update_not_found(self):
        response = self.client.post(
            reverse(
                "products:product-update",
                kwargs={"slug": "does-not-exist"},
            ),
            {
                "title": "New Product",
                "description": self.description,
                "price": self.price,
                "category": self.category.pk,
            },
        )

        # The requested product does not exist
        self.assertEqual(response.status_code, 404)

    # Test that updating the product does not remove its existing image
    def test_product_update_keeps_existing_image(self):
        response = self.client.post(
            reverse(
                "products:product-update",
                kwargs={"slug": self.product.slug},
            ),
            {
                "title": "Updated Product",
                "description": "Updated description",
                "price": 700,
                "category": self.new_category.pk,
            },
        )

        self.assertEqual(response.status_code, 302)

        # The existing image should still belong to the product
        self.assertTrue(
            ProductImage.objects.filter(
                product=self.product
            ).exists()
        )