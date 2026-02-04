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