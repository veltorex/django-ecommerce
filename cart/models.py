from django.db import models
from users.models import User
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    def __str__(self):
        return f"{self.user.email}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="quantity_positive",
            ),
        ]