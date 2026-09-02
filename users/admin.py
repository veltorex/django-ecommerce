from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Profile, Address

# Register your models here.

class UserAdmin(BaseUserAdmin):
    # Forms
    add_form = UserCreationForm
    form = UserChangeForm
    
    # Lists
    list_display = ["email", "is_superuser"]
    list_filter = ["is_superuser"]
    
    # Fieldsets
    fieldsets = (
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "is_active"]}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2", "is_active", "is_staff"],
            },
        ),
    )
    
    search_fields = ["email"]
    ordering = ["email"]

# Register User model to admin site
admin.site.register(User, UserAdmin)

# Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "phone_number"]
    search_fields = ["user__email", "first_name", "last_name"]
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "postal_code"]
    search_fields = ["user__email", "title", "postal_code"]
    
# Register
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)