from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import Product, Category
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          ProductWriteSerializer, CategorySerializer)
 
 
class ProductViewSet(viewsets.ModelViewSet):
    queryset           = Product.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter,
                          DjangoFilterBackend]
    search_fields      = ['name', 'description', 'category__name']
    ordering_fields    = ['price', 'created_at', 'name']
    filterset_fields   = ['category', 'is_active']
 
    def get_serializer_class(self):
        # Use different serializers for different actions
        if self.action == 'list':
            return ProductListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProductWriteSerializer
        return ProductDetailSerializer
 
    def get_queryset(self):
        qs = super().get_queryset().select_related('category')
        if self.action == 'retrieve':
            qs = qs.prefetch_related('tags')
        return qs
 
    def get_permissions(self):
        # Only admins can create/update/delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
 
    # Custom action: GET /api/products/featured/
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.get_queryset().filter(is_active=True)[:5]
        serializer = ProductListSerializer(featured, many=True,
                                          context={'request': request})
        return Response(serializer.data)
 
    # Custom action: POST /api/products/{id}/toggle-active/
    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAdminUser])
    def toggle_active(self, request, pk=None):
        product = self.get_object()
        product.is_active = not product.is_active
        product.save(update_fields=['is_active'])
        return Response({'is_active': product.is_active})
 




 
# ── LOW-LEVEL CACHE API ─────────────────────────────────────
from django.core.cache import cache
 	
# Cache a queryset for 15 minutes
def get_featured_products():
    key = 'featured_products'
    products = cache.get(key)
    if products is None:
        from shop.models import Product
        products = list(Product.objects.filter(is_active=True)[:5])
        cache.set(key, products, timeout=60*15)   # 15 minutes
    return products






# Invalidate cache when a product is saved
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Product
 
@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete('featured_products')
    cache.delete(f'product_detail_{instance.pk}')
 
 
# ── VIEW-LEVEL CACHE ────────────────────────────────────────
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
 
# Cache a function-based view for 15 minutes
@cache_page(60 * 15)
def product_list(request):
    ...
 
# Cache a class-based view
@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    ...
 
 
# ── CACHE IN DRF API ────────────────────────────────────────
from api.serializers import ProductListSerializer
from django.core.cache import cache
 
class ProductViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        cache_key = f'api_product_list_{request.query_params}'
        data = cache.get(cache_key)
        if data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=300)
            return response
        return Response(data)
