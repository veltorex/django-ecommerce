from django.urls import path
from .views import (
    product_list,
    product_detail,
    product_create,
    product_delete,
    product_update,
)

app_name = "products"

urlpatterns = [
    path("", product_list, name="product-list"),
    path("<slug>/", product_detail, name="product-detail"),
    path("create/", product_create, name="product-create"),
    path("delete/<slug>/", product_delete, name="product-delete"),
    path("<slug>/update/", product_update, name="product-update"),
]