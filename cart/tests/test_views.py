# cart/tests/test_views.py

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from cart.models import Cart, CartItem
from products.models import Category, Product
from users.models import User


class TestCartViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authenticated requests.
        cls.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
        )

        # Create a category and product for cart tests.
        cls.category = Category.objects.create(
            name="Test Category",
        )

        cls.product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            description="Test description",
            price=Decimal("100.00"),
            category=cls.category,
        )

        # Create another product to test carts containing multiple items.
        cls.product_2 = Product.objects.create(
            title="Test Product 2",
            slug="test-product-2",
            description="Test description",
            price=Decimal("50.00"),
            category=cls.category,
        )

    def setUp(self):
        # Log the user in before tests that require authentication.
        self.client.login(
            email="test@example.com",
            password="testpassword123",
        )

        # Create a cart for the logged-in user.
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_view_requires_login(self):
        # Anonymous users should be redirected to the login page.
        self.client.logout()

        response = self.client.get(reverse("cart:cart"))

        self.assertEqual(response.status_code, 302)

    def test_cart_view_returns_200_for_authenticated_user(self):
        # Authenticated users should be able to access the cart page.
        response = self.client.get(reverse("cart:cart"))

        self.assertEqual(response.status_code, 200)

    def test_cart_view_uses_correct_template(self):
        # The cart view should render the cart template.
        response = self.client.get(reverse("cart:cart"))

        self.assertTemplateUsed(response, "cart/cart.html")

    def test_cart_view_displays_cart_items(self):
        # The cart page should contain the user's cart items.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        response = self.client.get(reverse("cart:cart"))

        self.assertContains(response, self.product.title)

    def test_cart_view_calculates_subtotal(self):
        # Subtotal should equal product price multiplied by quantity.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3,
        )

        response = self.client.get(reverse("cart:cart"))

        cart_item = response.context["cart_items"][0]

        self.assertEqual(cart_item.subtotal, Decimal("300.00"))

    def test_cart_view_calculates_total(self):
        # Total should equal the sum of all cart item subtotals.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )
        CartItem.objects.create(
            cart=self.cart,
            product=self.product_2,
            quantity=3,
        )

        response = self.client.get(reverse("cart:cart"))

        self.assertEqual(response.context["total"], Decimal("350.00"))

    def test_add_to_cart(self):
        # Adding a product should create a CartItem with the requested quantity.
        response = self.client.post(
            reverse("cart:add", args=[self.product.id]),
            {"quantity": 3},
        )

        self.assertEqual(response.status_code, 302)

        cart_item = CartItem.objects.get(
            cart=self.cart,
            product=self.product,
        )

        self.assertEqual(cart_item.quantity, 3)

    def test_add_to_existing_cart_item_increases_quantity(self):
        # Adding an already-existing product should increase its quantity.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.client.post(
            reverse("cart:add", args=[self.product.id]),
            {"quantity": 3},
        )

        cart_item = CartItem.objects.get(
            cart=self.cart,
            product=self.product,
        )

        self.assertEqual(cart_item.quantity, 5)

    def test_decrease_quantity(self):
        # Decreasing an item should reduce its quantity by one.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3,
        )

        self.client.post(
            reverse("cart:decrease", args=[self.product.id]),
        )

        cart_item = CartItem.objects.get(
            cart=self.cart,
            product=self.product,
        )

        self.assertEqual(cart_item.quantity, 2)

    def test_remove_item(self):
        # Removing an item should delete it from the cart.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.client.post(
            reverse("cart:remove", args=[self.product.id]),
        )

        self.assertFalse(
            CartItem.objects.filter(
                cart=self.cart,
                product=self.product,
            ).exists()
        )

    def test_remove_item_requires_login(self):
        # Anonymous users should not be allowed to remove cart items.
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.client.logout()

        response = self.client.post(
            reverse("cart:remove", args=[self.product.id]),
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            CartItem.objects.filter(
                cart=self.cart,
                product=self.product,
            ).exists()
        )