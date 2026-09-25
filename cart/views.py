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

@login_required
def add_to_cart(request, id):
    # Only allow POST requests
    if request.method == "POST":
        # Get the quantity from the form
        quantity = int(request.POST.get("quantity", 1))

        # Get or create the user's cart
        cart, _ = Cart.objects.get_or_create(
            user=request.user
        )

        # Get or create the cart item
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=id,
            defaults={
                "quantity": quantity,
            },
        )

        # If the item already exists, increase its quantity
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        # Redirect to the cart page
        return redirect("cart:cart")

    # Return 404 for non-POST requests
    raise Http404

@login_required
def decrease_quantity(request, item_id):
    # Only allow POST requests
    if request.method != "POST":
        raise Http404

    # Get the cart item belonging to the user's cart
    item = get_object_or_404(
        CartItem,
        cart=request.user.cart,
        product_id=item_id,
    )

    # Decrease quantity if there is more than one item
    if item.quantity > 1:
        item.quantity -= 1
        item.save(update_fields=["quantity"])

    # Remove the item if its quantity is one
    else:
        item.delete()

    # Redirect back to the cart
    return redirect("cart:cart")