from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/',               views.cart_detail,   name='detail'),
    path('add/<int:pk>/',  views.cart_add,       name='cart_add'),
    path('remove/<int:pk>/', views.cart_remove,  name='cart_remove'),
    path('inc/<int:pk>/',  views.cart_increment, name='cart_increment'),  
    path('dec/<int:pk>/',  views.cart_decrement, name='cart_decrement'),  
]