from django.contrib import admin

# Register your models here.
from .models import HomeHero, Product

admin.site.register(HomeHero)
admin.site.register(Product)