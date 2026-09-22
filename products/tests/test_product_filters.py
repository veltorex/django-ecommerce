# products/tests/test_product_filters.py

from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from ..models import Product, Category

class TestProductFilters(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(12):
            category = Category.objects.create(name=f"Test Category {i}")
            Product.objects.create(
                title=f"Test {i}",
                description=f"Test description {i}",
                price=300 + i,
                category=category,
            )

    # Test with filtering products
    def test_product_filters(self):
        # Define URL
        url = reverse("products:product-list")

        # Add query parameters to URL
        url += "?min_price=302&max_price=306&category=2&category=3&category=4&category=5&category=6&category=7&sort=price_low"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check the result
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["min_price"], "302")
        self.assertEqual(response.context["max_price"], "306")
        self.assertEqual(products.paginator.count, 5)
        self.assertEqual(response.context["selected_category"], ["2", "3", "4", "5", "6", "7"])
        self.assertEqual(response.context["sort_by"], "price_low")
        self.assertEqual(products[0].price, Decimal("302.00"))
        self.assertEqual(products[-1].price, Decimal("306.00"))

    # Test with newest sort filter
    def test_product_filters_sort_newest(self):        
        ##### Newest #####

        # Define URL
        url = reverse("products:product-list")       

        # Add newest sort query parameter
        url += "?sort=newest"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)

        # Check if the results are sorted

        sorted_products = list(products.object_list)
        sorted_products.sort(key=lambda product: product.created_at, reverse=True)

        self.assertEqual(sorted_products, products.object_list)

    # Test with price low sort filter
    def test_products_filters_sort_price_low(self):
        #####‌ Price Low #####

        # Define URL
        url = reverse("products:product-list")       

        # Add price low sort query parameter
        url += "?sort=price_low"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)

        # Check if the results are sorted

        sorted_products = list(products.object_list)
        sorted_products.sort(key=lambda product: product.price)

        self.assertEqual(sorted_products, products.object_list)    

    # Test with price high sort filter
    def test_product_filters_sort_price_high(self):
        # Define URL
        url = reverse("products:product-list")

        # Add price high sort query parameter
        url += "?sort=price_high"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)

        # Check if the results are sorted
        sorted_products = list(products.object_list)
        sorted_products.sort(
            key=lambda product: product.price,
            reverse=True
        )

        self.assertEqual(sorted_products, products.object_list)


    # Test with min price filter
    def test_product_filters_min_price(self):
        # Define URL
        url = reverse("products:product-list")       

        # Add min price query parameter
        url += "?min_price=305"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        #‌ Check the result
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products[0].price, Decimal("305.00"))

    # Test with max price filter    
    def test_product_filters_max_price(self):
        # Define URL
        url = reverse("products:product-list")       

        # Add max price query parameter
        url += "?max_price=310"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check the result
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products[-1].price, Decimal("310.00"))

    # Test with empty filter
    def test_product_filters_empty(self):
        # Define URL
        url = reverse("products:product-list")       

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(products.object_list), list(Product.objects.all()))

    # Test empty result
    def test_product_filters_empty_result(self):
        # Define URL
        url = reverse("products:product-list")       

        # Add min price query parameter
        url += "?min_price=1000"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products.paginator.count, 0)

    # Test search
    def test_product_filters_search(self):
        # Define URL
        url = reverse("products:product-list")

        # Add q query parameter
        url += "?q=Test 5"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products.paginator.count, 1)
        self.assertEqual(products[0].title, "Test 5")

    # Test search in product description
    def test_product_filters_search_description(self):
        # Define URL
        url = reverse("products:product-list")

        # Add q query parameter
        url += "?q=description 5"

        # Send request to product list page
        response = self.client.get(url)

        # Get products
        products = response.context["products"]

        # Check results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products.paginator.count, 1)
        self.assertEqual(products[0].title, "Test 5")
    