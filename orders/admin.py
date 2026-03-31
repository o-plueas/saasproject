from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'total']
    search_fields = ['user', 'status', 'total']
    list_filter = ['user', 'status', 'total']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['quantity']

