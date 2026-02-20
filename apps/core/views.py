import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
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


# --- Cart & Checkout Views ---

def cart_page(request):
    """
    Renders the cart/checkout page.
    Fetches user addresses if they are logged in.
    """
    addresses = []
    if request.user.is_authenticated:
        addresses = Address.objects.filter(user=request.user)
    
    return render(request, 'cart.html', {'addresses': addresses})


@login_required
def add_address(request):
    """
    Handles the submission of the 'Add New Address' modal form.
    """
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        is_default = request.POST.get('is_default') == 'on'

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            street_address=street_address,
            city=city,
            state=state,
            pincode=pincode,
            is_default=is_default
        )
        messages.success(request, "New delivery address added successfully.")
        return redirect('cart_page')
    
    return redirect('cart_page')


@login_required
def place_order(request):
    """
    Receives JSON data from Alpine.js via fetch API to create the final order.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_items = data.get('cart', [])
            address_id = data.get('address_id')
            subtotal = data.get('subtotal')
            delivery_fee = data.get('delivery_fee', 0)
            total = data.get('total')

            # Get the selected address
            shipping_address = Address.objects.get(id=address_id, user=request.user)

            # Create the main Order
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total_amount=total,
                status='Pending'
            )

            # Create Order Items
            for item in cart_items:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price, # Record the price at the time of purchase
                    quantity=item['quantity']
                )

            return JsonResponse({'success': True, 'message': 'Order placed successfully!', 'order_id': order.id})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})