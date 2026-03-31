from celery  import shared_task 
from django.contrib.auth import get_user_model 

@shared_task 
def send_welcome_email_task(user_id):
    """
    Celery task to send welcome email asynchronously.
    We pass user_id (not the user object) because Celery serializes args to JSON.
    """
      
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        from .email import send_welcome_email 
        send_welcome_email(user)
    except User.DoesNotExist:
        pass 

@shared_task
def add(a):
    return a + a + a+ a






@shared_task 
def send_login_email_task(user_id):
    """
    Celery task to send welcome email asynchronously.
    We pass user_id (not the user object) because Celery serializes args to JSON.
    """
      
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        from .email import send_login_email 
        send_login_email(user)
    except User.DoesNotExist:
        pass 
