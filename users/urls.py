from django.urls import path, include
from .views import register, profile, edit_profile, address_list, add_address

app_name = "users"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit-profile"),
    path("addresses/", address_list, name="address-list"),
    path("addresses/add/", add_address, name="add-address")
]