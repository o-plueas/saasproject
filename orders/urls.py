from django.urls import path
from . import views 


app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path('order_sucess/<int:pk>/', views.order_sucess, name="order_sucess"),
    # path('payment/init/<int:order_id>/', views.initialize_payment, name='payment_init'),
    path('payment/verify/<int:order_id>/', views.verify_payment, name='payment_verify'),
    path('order-detail/<int:pk>', views.order_detail, name="orderdetail"),
    path('allorders/', views.all_orders, name="allorders")


    
]