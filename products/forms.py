from django import forms
from .models import Product, ProductImage


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("title", "description", "price")

