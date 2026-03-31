# accounts/email.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(user):
    """
    Send a welcome email to a new user after registration.
    """
    subject = f"Welcome to MyShop, {user.get_full_name() or user.username}!"
    context = {
        "user": user,
    }

    # Plain text version
    text_body = render_to_string("emails/welcome.txt", context)

    # HTML version
    html_body = render_to_string("emails/welcome.html", context)

    # Create the email 
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    # Attach HTML alternative
    msg.attach_alternative(html_body, "text/html")

    # Send email
    msg.send()








def send_login_email(user):
    """
    Send a welcome email to a new user after registration.
    """
    subject = f"New Login to MyShop, {user.get_full_name() or user.username}!"
    context = {
        "user": user,
    }

    # Plain text version
    text_body = render_to_string("emails/login_email.txt", context)

    # HTML version
    html_body = render_to_string("emails/login_email.html", context)

    # Create the email 
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    # Attach HTML alternative
    msg.attach_alternative(html_body, "text/html")

    # Send email
    msg.send()