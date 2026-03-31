from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

 
# In checkout view — call task asynchronously
from orders.tasks import send_order_confirmation_task
 
def checkout(request, order_id):
    pass
    from orders.models import Order
    from orders.emails import send_order_confirmation
    order = Order.objects.select_related('user').prefetch_related(
        'items__product').get(pk=order_id)
    # ...create order...
    # .delay() sends the task to Redis queue — does NOT block
    send_order_confirmation_task.delay(order.pk)
    messages.success(request, 'Order placed! Confirmation email on its way.')
    return redirect('orders:detail', pk=order.pk)
 
