from django import forms
from .models import Product, ProductImage


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("title", "description", "price")


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image",)
