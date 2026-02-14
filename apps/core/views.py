from django.shortcuts import render
from .models import *

def home(request):
    slides = HomeHero.objects.order_by('order')
    products = Product.objects.all()
    return render(request, 'index.html', {'slides': slides, 'products': products})