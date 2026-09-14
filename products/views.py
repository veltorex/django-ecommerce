from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductImageFormSet, ProductForm
from .filters import filter_products

# Create your views here.

def product_list(request):
    products  = Product.objects.all()
    categories = Category.objects.all()
    
    # Search
    query = request.GET.get("q", "").strip()
    products = filter_products(products, query)
    
    # Filtering
    selected_category = request.GET.getlist("category")
    
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    
    sort_by = request.GET.get("sort")
    
    if selected_category:
        products = products.filter(category_id__in=selected_category)
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    if sort_by == "price-low":
        products = products.order_by("price")
    elif sort_by == "price-high":
        products = products.order_by("-price")
    elif sort_by == "newest": 
        products = products.order_by("-created_at")

    # Pagination

    paginator = Paginator(products, 24)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    return render(
        request,
        "products/product_list.html",
        {
            "products": page_obj,
            "categories": categories,
            "selected_category": selected_category,
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by,
            "query": query,
            "query_params": query_params,
        }
    )
    

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
        }
    )
    
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()

            formset.instance = product
            formset.save()

            return redirect("products:product-list")

    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(
        request,
        "products/product_create.html",
        {
            "form": form,
            "formset": formset,
        },
    )
    
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug) # If the object doesn't exist, it returns an HTTP 404 error page.
    
    if request.method == "POST":
        
        product.delete()
        return redirect("products:product-list")
    
    return render(request, "products/product_delete.html", {"product": product})

def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)  # Use the existing product instance
        
        if form.is_valid():
            form.save()
            return redirect("products:product-list")
        
    else:
        form = ProductForm(instance=product)
        
    return render(
        request,
        "products/product_update.html",
        {"form": form},
    )