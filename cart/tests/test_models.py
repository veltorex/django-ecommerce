# cart/tests/test_models.py

from django.db import IntegrityError
from django.test import TestCase

from ..models import Cart, CartItem
from products.models import Product, Category
from users.models import User


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create(
            email="test1234@gmail.com",
            password="test1234",
        )

        # Create a cart for the user
        cls.cart = Cart.objects.create(
            user=cls.user,
        )

        # Create a category for the test product
        cls.category = Category.objects.create(
            name="Category",
        )

        # Create a test product
        cls.product = Product.objects.create(
            title="Product",
            description="Product description",
            price=100,
            category=cls.category,
        )

        # Create a cart item
        cls.cart_item = CartItem.objects.create(
            product=cls.product,
            cart=cls.cart,
            quantity=1,
        )

    # ---------------------------------------------------------
    # Cart tests
    # ---------------------------------------------------------

    # Test that a user cannot have more than one cart
    def test_cart_one_to_one_relationship(self):
        with self.assertRaises(IntegrityError):
            Cart.objects.create(
                user=self.user,
            )

    # Test the relationship between Cart and User
    def test_cart_user_relationship(self):
        # Check the relationship from Cart to User
        self.assertEqual(
            self.cart.user,
            self.user,
        )

        # Check the reverse relationship from User to Cart
        self.assertEqual(
            self.user.cart,
            self.cart,
        )

    # Test that deleting a user also deletes their cart
    def test_delete_user_deletes_cart(self):
        self.user.delete()

        # User should no longer exist
        self.assertFalse(
            User.objects.filter(
                email="test1234@gmail.com",
            ).exists()
        )

        # The user's cart should also be deleted
        self.assertFalse(
            Cart.objects.filter(
                pk=self.cart.pk,
            ).exists()
        )

        # Cart items belonging to the deleted cart
        # should also be deleted if CartItem.cart uses CASCADE
        self.assertFalse(
            CartItem.objects.filter(
                pk=self.cart_item.pk,
            ).exists()
        )

    # ---------------------------------------------------------
    # CartItem tests
    # ---------------------------------------------------------

    # Test the relationship between CartItem and Cart
    def test_cart_item_cart_relationship(self):
        self.assertEqual(
            self.cart_item.cart,
            self.cart,
        )

        # Check the reverse relationship
        self.assertIn(
            self.cart_item,
            self.cart.items.all(),
        )

    # Test the relationship between CartItem and Product
    def test_cart_item_product_relationship(self):
        self.assertEqual(
            self.cart_item.product,
            self.product,
        )

        # Check the reverse relationship
        self.assertIn(
            self.cart_item,
            self.product.cart_items.all(),
        )

    # Test the default quantity of a CartItem
    def test_cart_item_default_quantity(self):
        # Create another product because the combination
        # of cart + product must be unique
        product = Product.objects.create(
            title="Product 2",
            description="Product 2 description",
            price=200,
            category=self.category,
        )

        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=product,
        )

        # Quantity should be 1 by default
        self.assertEqual(
            cart_item.quantity,
            1,
        )

    # Test that the same product cannot be added
    # to the same cart as another CartItem
    def test_unique_product_per_cart(self):
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                cart=self.cart,
                product=self.product,
                quantity=2,
            )

    # Test that the same product can exist
    # in different carts
    def test_same_product_in_different_carts(self):
        # Create another user
        user = User.objects.create(
            email="test5678@gmail.com",
            password="test5678",
        )

        # Create another cart for the second user
        cart = Cart.objects.create(
            user=user,
        )

        # The same product should be allowed
        # in another cart
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=1,
        )

        self.assertEqual(
            cart_item.product,
            self.product,
        )

        self.assertEqual(
            cart_item.cart,
            cart,
        )

    # Test that deleting a cart also deletes its cart items
    def test_delete_cart_deletes_cart_items(self):
        self.cart.delete()

        # Cart should be deleted
        self.assertFalse(
            Cart.objects.filter(
                pk=self.cart.pk,
            ).exists()
        )

        # Cart item should also be deleted
        # if CartItem.cart uses CASCADE
        self.assertFalse(
            CartItem.objects.filter(
                pk=self.cart_item.pk,
            ).exists()
        )

    # ---------------------------------------------------------
    # Quantity constraint tests
    # ---------------------------------------------------------
    #
    # Keep these tests ONLY if your CartItem model has
    # a CheckConstraint that requires quantity > 0.
    #

    # Test that quantity cannot be zero
    def test_cart_item_zero_quantity(self):
        product = Product.objects.create(
            title="Product 3",
            description="Product 3 description",
            price=300,
            category=self.category,
        )

        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                cart=self.cart,
                product=product,
                quantity=0,
            )

    # Test that quantity cannot be negative
    def test_cart_item_negative_quantity(self):
        product = Product.objects.create(
            title="Product 4",
            description="Product 4 description",
            price=400,
            category=self.category,
        )

        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                cart=self.cart,
                product=product,
                quantity=-10,
            )