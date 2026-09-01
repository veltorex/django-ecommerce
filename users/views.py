from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product-list")
        
    else:
        form = UserCreationForm()
        
    return render(request, "registration/register.html", {"form": form})
        