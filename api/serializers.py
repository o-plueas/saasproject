from rest_framework import serializers
from shop.models import Product, Category, Tag
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model
 
User = get_user_model()
 
 
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name']
 
 
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)  # from annotate
 
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'product_count']
 
 
class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2,
                                               read_only=True)
 
    class Meta:
        model  = Product
        fields = ['id', 'name', 'slug', 'price', 'effective_price',
                  'image', 'stock', 'category_name', 'is_active']
 
 
class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view — includes nested tags."""
    category = CategorySerializer(read_only=True)
    tags     = TagSerializer(many=True, read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2,
                                               read_only=True)
 
    class Meta:
        model  = Product
        fields = ['id', 'name', 'slug', 'description', 'price',
                  'effective_price', 'sale_price', 'stock', 'image',
                  'category', 'tags', 'is_active', 'created_at']
 
 
class ProductWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products."""
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'sale_price',
                  'stock', 'image', 'category', 'tags', 'is_active']
 
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value
 
    def validate(self, data):
        if data.get('sale_price') and data['sale_price'] >= data.get('price', 0):
            raise serializers.ValidationError({
                'sale_price': 'Sale price must be less than original price.'
            })
        return data
 
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        product = Product.objects.create(**validated_data)
        product.tags.set(tags)
        return product
 
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance









