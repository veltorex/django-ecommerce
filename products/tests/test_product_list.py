# products/tests/test_product_list.py

from django.test import TestCase
from django.urls import reverse

from ..models import Product, Category


class ProductListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Test Category"
        )

        # Create 25 products so that we have two pages
        for i in range(25):
            Product.objects.create(
                title=f"Product {i}",
                description=f"Description {i}",
                price=100 + i,
                category=cls.category,
            )

    # Test that the first page contains the correct number of products
    def test_product_list_first_page(self):
        response = self.client.get(
            reverse("products:product-list")
        )

        self.assertEqual(response.status_code, 200)

        # The first page should contain 24 products
        self.assertEqual(
            len(response.context["products"]),
            24,
        )

    # Test the second page
    def test_product_list_second_page(self):
        response = self.client.get(
            reverse("products:product-list") + "?page=2"
        )

        self.assertEqual(response.status_code, 200)

        # The second page should contain the remaining product
        self.assertEqual(
            len(response.context["products"]),
            1,
        )

    # Test that page 1 has a next page
    def test_product_list_has_next_page(self):
        response = self.client.get(
            reverse("products:product-list")
        )

        self.assertTrue(
            response.context["products"].has_next()
        )

    # Test that the last page has no next page
    def test_product_list_last_page(self):
        response = self.client.get(
            reverse("products:product-list") + "?page=2"
        )

        self.assertFalse(
            response.context["products"].has_next()
        )

    # Test an invalid page number
    def test_product_list_invalid_page(self):
        response = self.client.get(
            reverse("products:product-list") + "?page=999"
        )

        self.assertEqual(response.status_code, 200)

        # Invalid page numbers should show the last page
        self.assertEqual(
            response.context["products"].number,
            2,
        )

        # The last page contains the remaining product
        self.assertEqual(
            len(response.context["products"]),
            1,
        )