from django.db import models
from django.utils.text import slugify
import PIL

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # create slug field
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)