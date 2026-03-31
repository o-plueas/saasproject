from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings 

def send_order_confirmation(order):
    subject = f'Order Confirmed - #{order.pk}'
    context = {'order': order, 'items': order.items.select_related('product').all()}
    
    # plain text version 

    text_body = render_to_string('emails/order_confirmation.txt', context)

    # HTML VERSION

    html_body = render_to_string("emails/order_confirmation.html", context)

    msg = EmailMultiAlternatives(
        subject = subject,
        body = text_body,
        from_email= settings.DEFAULT_FROM_EMAIL,
        to = [order.user.email],

    )

    msg.attach_alternative(html_body, 'text/html')
    msg.send()






