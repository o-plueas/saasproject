# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/notifications/',      views.get_notifications, name='get_notifications'),
    path('api/notifications/read/', views.mark_all_read,     name='mark_all_read'),
]