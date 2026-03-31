from django.db import models
from django.conf import settings

from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True,)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True,)    


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    # ✅ nullable so effective_price logic works correctly
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    
    categories = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    # ✅ related_name fixed — was "tags" (clashes with Tag model reverse)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products", null=True, blank=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def effective_price(self):
        # ✅ sale_price is now nullable, so this check is safe
        return self.sale_price if self.sale_price is not None else self.price

    def is_in_stock(self):
        return self.stock > 0



        