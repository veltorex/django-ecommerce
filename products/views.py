from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductImageFormSet, CreateProductForm

# Create your views here.

def product_list(request):
    products  = Product.objects.all()
    
    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
        }
    )
    
    
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
        }
    )
    
def product_create(request):
    if request.method == "POST":
        form = CreateProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()

            formset.instance = product
            formset.save()

            return redirect("product-list")

    else:
        form = CreateProductForm()
        formset = ProductImageFormSet()

    return render(
        request,
        "products/product_create.html",
        {
            "form": form,
            "formset": formset,
        },
    )