from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
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
    