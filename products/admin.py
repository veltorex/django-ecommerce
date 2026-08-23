from django.contrib import admin
from .models import Product, ProductImage


# Add product image form to product form
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image",)
    max_num = 10
    min_num = 1


# Customize product admin form
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["title", "description", "price", "slug"]
    readonly_fields = ("slug",)

    list_display = ("title", "price", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    
    inlines = [ProductImageInline]