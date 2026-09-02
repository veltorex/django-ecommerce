from django.urls import path, include
from .views import register, profile, edit_profile

app_name = "users"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit-profile"),
]