from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .models import *

# --- Main Home View ---
def home(request):
    slides = HomeHero.objects.order_by('order')
    products = Product.objects.all()
    return render(request, 'index.html', {'slides': slides, 'products': products})

# --- Authentication Views ---
def signup_view(request):
    # Agar user pehle se login hai, toh usko wapas home page par bhej do
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Signup ke turant baad user ko automatically login karwana
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to Daillyfresh.")
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    # Agar user pehle se login hai, toh usko wapas home page par bhej do
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')