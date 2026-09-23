from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart

# Create your views here.

@login_required
def cart_view(request):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # Get cart items
    cart_items = cart.items.select_related("product")

    # Render template
    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
        },
    )