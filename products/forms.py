from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("title", "description", "price", "category")


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image",)

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    fields=("image",),
    extra=10,
    max_num=10,
)