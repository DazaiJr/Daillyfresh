from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Product

def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'index.html', {'products': products})

def login(request):
    return render(request,'login.html')

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required!')
            return render(request, 'register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return render(request, 'register.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'This email is already registered!')
            return render(request, 'register.html')
        
        # Create user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'register.html')
    
    return render(request, 'register.html')