from django.db import models
from .services.image import process_product_image
from .services.slug import create_unique_slug

# Create your models here.

# Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self.title, Product)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/", max_length=255)
    
    
    
    def save(self, *args, **kwargs):
        processed_image = process_product_image(self.image)

        self.image.save(
            self.image.name.rsplit(".", 1)[0] + ".jpg",
            processed_image,
            save=False,
        )

        super().save(*args, **kwargs)