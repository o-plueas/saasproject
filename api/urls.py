
# api/urls.py
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.urls import path
 
router = DefaultRouter()
router.register('products',   views.ProductViewSet,  basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('orders',     views.OrderViewSet,    basename='order')
 
urlpatterns = [
    *router.urls,
    path('auth/token/',         TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),    name='token-refresh'),
]
