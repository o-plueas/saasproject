from notifications.utils import send_notification 
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect 

from cart.cart import Cart
from .models import Order, OrderItem 
from shop.models import Product 
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import F, Sum
import requests

from cart.cart import Cart
from .models import Order, OrderItem



# ✅ Fix 1: calculate total server-side, never from POST
# ✅ Fix 2: requests.post (not request.post) in initialize_payment

def checkout(request):
    from django.shortcuts import render
    cart = Cart(request)

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == "POST":
        # with transaction.atomic() #indent next block 
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            total=0,  # placeholder; calculated below
        )  
        
          # ✅ send notification to that user
        send_notification(
            request.user.pk,
            "New Order",
            f"Order #{order.pk} created successfully",
            "success"
        )

        for item in cart.get_items():
            product = item['product']
            quantity = item['qty']
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['product'].effective_price,
                quantity=quantity,
            )


        product.stock -= quantity
        if product.stock < 0:
            product.stock = 0
        product.save()


        order.calculate_total()  # ✅ always server-side


        cart.clear()

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": order.user.email,
            "amount": int(order.total * 100),
            "callback_url": request.build_absolute_uri(f"/orders/payment/verify/{order.id}/"),
            "reference": f"ORD{order.id}{order.user.id}",
        }

        import requests
        response = requests.post(url, json=data, headers=headers)  # ✅ requests not request
        res_data = response.json()

        if res_data['status']:
            return redirect(res_data['data']['authorization_url'])
        else:
            return redirect('orders:checkout')

    return render(request, "orders/checkout.html", {"cart": cart})



def order_sucess(request, pk):
    return render(request, 'orders/sucess.html')
        



# import requests 
# from django.conf import settings 
# from django.db.models import F, Sum

# def initialize_payment(request, pk):

#     order = Order.objects.get(pk=pk)

#     url = "https://api.paystack.co/transaction/initialize"
#     headers = {
#         "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
#         "Content-Type": "application/json",

#     }
#     data = {
#         "email": order.user.email,
#         "amount": int(order.items.aggregate(total=Sum(F('price') * F('quantity')))['total'] * 100),
#         "callback_url": request.build_absolute_uri(f"/orders/payment/verify/{order.id}"),
#         "reference": f"ORD{order.id}{order.user.id}",
#     }

#     response = request.post(url, json=data, headers=headers)
#     res_data = response.json()


#     if res_data['status']:
#         return redirect(res_data['data']['authorization_url'])
#     else:
#         # handle error
#         return redirect('orders:checkout')
    



# orders/views.py
def verify_payment(request, order_id):
    order = Order.objects.get(pk=order_id)

    reference = request.GET.get('reference')  # Paystack reference
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data['status'] and res_data['data']['status'] == 'success':
        
        if order.status != Order.STATUS_PAID:

            # Payment successful
            order.status = Order.STATUS_PAID
            order.save()

            # Reduce stock
            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()

            # Send email via celery no signal 
            from .tasks import send_order_confirmation_task
            send_order_confirmation_task.delay(order.id)

            return redirect('orders:success', order_id=order.id)
    else:
        # Payment failed
        order.status = Order.STATUS_PENDING
        order.save()
        return redirect('orders:failed', order_id=order.id)



@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    orderitems = OrderItem.objects.filter(order=order)

    context = {
        'orderitems': orderitems,
        'order':order
    }


    return render(request, 'orders/order-detail.html', context)

from django.db.models import Prefetch

def all_orders(request):

    # orders = Order.objects.all().prefetch_related(
    #     Prefetch("items", queryset=OrderItem.objects.prefetch_related("product"))
    # )

    # from django.contrib.auth import get_user_model

    # User  = get_user_model() 
    # vendor = User.objects.filter(role="vendor").first
    user = request.user 


    if user.role == 'admin':
        orders = Order.objects.all().prefetch_related("items__product")

    elif user.role == 'vendor':


        # Order → OrderItem → Product → Product.user (vendor)
        # orders = OrderItem.objects.filter(product__user=vendor)
       

        orders = Order.objects.filter(items__product__user=user).distinct().prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.filter(product__user=user).select_related("product"))
        )

    else:

        orders = Order.objects.filter(user=user).prefetch_related("items__product")

    return render(request, "orders/orders.html", {"orders":orders})

