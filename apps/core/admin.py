from django.contrib import admin

# Register your models here.
from .models import HomeHero, Product, Address, Order, OrderItem

admin.site.register(HomeHero)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)