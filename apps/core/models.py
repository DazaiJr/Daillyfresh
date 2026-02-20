from django.db import models
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.
class HomeHero(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    image = models.ImageField(upload_to='hero/')
    show_button = models.BooleanField(default=True)
    order = models.IntegerField(default=0)


# @receiver(post_delete, sender=HomeHero)
# def delete_image_file(sender, instance, **kwargs):
#     if instance.image:
#         instance.image.delete(save=False)


# Products model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, help_text="e.g., 1000 ml, 500 gm")
    image = models.ImageField(upload_to='products/')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    # is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviews_count = models.IntegerField(default=5)
    badge = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 'Best Seller', 'New Arrival'")
    # updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
# --- Address Model ---
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.city} ({self.pincode})"

    def save(self, *args, **kwargs):
        # Ensure only one default address exists per user
        if self.is_default:
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)


# --- Order Model ---
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username if self.user else 'Guest'}"


# --- Order Item Model ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Store price at the time of purchase
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Deleted Product'} (Order #{self.order.id})"
    
    def get_cost(self):
        return self.price * self.quantity