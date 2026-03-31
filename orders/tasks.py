
 
# orders/tasks.py — async tasks for the SaaS project
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
 
@shared_task(bind=True, max_retries=3)
def send_order_confirmation_task(self, order_id):
    """Send order confirmation email — runs in background worker."""
    try:
        from orders.models import Order
        from orders.emails import send_order_confirmation
        order = Order.objects.select_related('user').prefetch_related(
            'items__product').get(pk=order_id)
        send_order_confirmation(order)
    except Exception as exc:
        # Retry after 60s, up to 3 times
        raise self.retry(exc=exc, countdown=60)
 
 
@shared_task
def send_low_stock_alert():
    """Periodic task: email admin if any product stock < 5."""
    from shop.models import Product
    from django.db.models import Q
    low = Product.objects.filter(stock__lt=5, is_active=True)
    if low.exists():
        product_list = ', '.join(p.name for p in low)
        send_mail(
            subject = 'Low Stock Alert',
            message = f'These products are low on stock: {product_list}',
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.ADMIN_EMAIL],
        )
