from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Tag

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'slug']
    search_fields = ['name', 'description']
    list_filter = ['name', 'price']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name']
    


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']














