from django.shortcuts import render

# Create your views here.
# pip install requests  # for Paystack
# OR
# pip install stripe
 
# ── PAYSTACK INTEGRATION ────────────────────────────────────
 
# payments/views.py
import requests
from django.contrib import messages
import hashlib
import hmac
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
 
@login_required
def initiate_payment(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, user=request.user)
 
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type':  'application/json',
    }
    payload = {
        'email':        request.user.email,
        'amount':       int(order.total * 100),  # Paystack uses kobo
        'reference':    f'order-{order.pk}-{order.created_at.timestamp():.0f}',
        'callback_url': request.build_absolute_uri('/payments/verify/'),
        'metadata': {
            'order_id':   order.pk,
            'user_email': request.user.email,
        }
    }
 
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    data = response.json()
 
    if data['status']:
        return redirect(data['data']['authorization_url'])
    else:
        messages.error(request, 'Payment initiation failed. Try again.')
        return redirect('orders:detail', pk=order.pk)
 
 
# ── WEBHOOK HANDLER — receives payment confirmation from Paystack ──
@csrf_exempt   # Paystack sends POST without CSRF token
def paystack_webhook(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
 
    # Step 1: Verify webhook signature — NEVER skip this
    signature = request.headers.get('X-Paystack-Signature', '')
    computed  = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        request.body,
        hashlib.sha512
    ).hexdigest()
 
    if not hmac.compare_digest(signature, computed):
        return HttpResponseBadRequest('Invalid signature')
 
    # Step 2: Parse the event
    event = json.loads(request.body)
 
    if event['event'] == 'charge.success':
        metadata = event['data']['metadata']
        order_id = metadata.get('order_id')
 
        try:
            order = Order.objects.get(pk=order_id)
            if order.status == Order.STATUS_PENDING:
                order.status = Order.STATUS_PROCESSING
                order.save(update_fields=['status'])
                # Trigger async notification
                from orders.tasks import send_order_confirmation_task
                send_order_confirmation_task.delay(order.pk)
        except Order.DoesNotExist:
            pass
 
    return JsonResponse({'received': True})
