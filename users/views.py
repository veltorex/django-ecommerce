from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, ProfileForm, AddressForm
from .models import Profile

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Create user profile
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("product-list")
        
    else:
        form = UserCreationForm()
        
    return render(request, "registration/register.html", {"form": form})
        
@login_required
def profile(request):
    profile = request.user.profile
    
    return render(request, "registration/profile.html", {"profile": profile})
    
@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect("profile")
        
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, "registration/edit_profile.html", {"form": form})

@login_required
def address_list(request):
    addresses = request.user.addresses.all()
    
    return render(request, "users/address_list.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("address-list")
        
    else:
        form =  AddressForm()
        
    return render(request, "users/add_address.html", {"form": form})
        

@login_required
def delete_address(request, pk):
    address = get_object_or_404(request.user.addresses, pk=pk)
    
    if request.method == "POST":
        address.delete()
        
    return redirect("address-list")

@login_required
def edit_address(request, pk):
    address = get_object_or_404(
        request.user.addresses,
        pk=pk,
    )

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            return redirect("address-list")
    else:
        form = AddressForm(instance=address)

    return render(
        request,
        "users/edit_address.html",
        {"form": form},
    )