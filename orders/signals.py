from django.db.models.signals import post_save 
from django.dispatch import receiver 
from django.conf import settings
from .models import Order 

# commeted will remove later because we don't need the signal for conditional logic like orders 

# @receiver(post_save, sender=Order)
# def order_confirmation_handler(sender, instance, created, **kwargs):
#     if created:
#         pass
#         try:
#             from .tasks import send_order_confirmation_task
#             send_order_confirmation_task(instance.pk)
#         except Exception as e:
#             print(f"Order Confirmation email failed: {e}")



# for test 
@receiver(post_save, sender=Order)
def debug_order(sender, instance, created, **kwargs):
    print("SIGNAL TRIGGERED:", instance.id, created)


@receiver(post_save, sender=Order)
def test_email(sender, instance, created, **kwargs):
    if created:
        from .emails import send_order_confirmation
        send_order_confirmation(instance)