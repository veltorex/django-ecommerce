from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Cart, CartItem

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

@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=request.user.cart,
        )

        item.delete()

        return redirect("cart:cart")

    raise Http404