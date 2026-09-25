from django.urls import path
from .views import cart_view, remove_from_cart, add_to_cart

app_name = "cart"

urlpatterns = [
    path("", cart_view, name="cart"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove"),
    path("add/<int:id>/", add_to_cart, name="add"),
]
