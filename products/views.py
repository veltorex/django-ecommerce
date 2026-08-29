from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductImageFormSet, CreateProductForm

# Create your views here.

def product_list(request):
    products  = Product.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
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
    
def prodcut_delete(request, pk):
    product = get_object_or_404(Product, pk=pk) # If the object doesn't exist, it returns an HTTP 404 error page.
    
    if request.method == "POST":
        
        product.delete()
        return redirect("product-list")
    
    return render(request, "products/product_delete.html", {"product": product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = CreateProductForm(request.POST, instance=product)  # Use the existing product instance
        
        if form.is_valid():
            form.save()
            return redirect("product-list")
        
    else:
        form = CreateProductForm(instance=product)
        
    return render(
        request,
        "products/product_update.html",
        {"form": form},
    )