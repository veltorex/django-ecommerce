from django.urls import path
from .views import product_list, product_detail, product_create, prodcut_delete

urlpatterns = [
    path("", product_list, name="product-list"),
    path("<int:pk>/", product_detail, name="product-detail"),
    path("create/", product_create, name="product-create"),
    path("delete/", prodcut_delete, name="product-delete"),
]