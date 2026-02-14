from django.db import models
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


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