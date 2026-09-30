from django.contrib import admin
from .models import Cart, CartItem


# Customize CartItem as an inline admin model
class CartItemInline(admin.TabularInline):
    model = CartItem

    # Fields displayed in the inline form
    fields = ["product", "quantity"]

    # Number of extra empty forms
    extra = 0


# Register and customize Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    # Search Cart by user's email
    search_fields = ["user__email"]

    # Display CartItems inside the Cart admin page
    inlines = [CartItemInline]


# Register and customize CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    # Fields displayed in the CartItem list
    list_display = ["cart", "product", "quantity"]

    # Filters in the sidebar
    list_filter = ["product"]

    # Search CartItems by user's email or product name
    search_fields = ["cart__user__email", "product__title"]

    # Default ordering
    ordering = ["cart", "product"]