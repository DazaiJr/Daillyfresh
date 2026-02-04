from django.shortcuts import render
from .models import *

def home(request):
    slides = HomeHero.objects.order_by('order')
    return render(request, 'index.html', {'slides': slides})