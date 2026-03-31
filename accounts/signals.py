from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.conf import settings 
from allauth.account.signals import user_signed_up
# Decrement stock when an order item is saved


User = settings.AUTH_USER_MODEL 

# Automatically send welcome email when a new user registers
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created_handler(sender, instance, created, **kwargs):
    if created:      
        pass
        # only on new user not update 
        # from .email import send_welcom_email
        try:
            from .tasks import send_welcome_email_task
            send_welcome_email_task.delay(instance.pk) # pass id not objec
        except Exception as e:
                        # Never let email failure break registration
            print(f'Welcome email failed: {e}')








# Automatically send welcome email when a  user logs in dot use post_save()
# use  user_logged_in  

from django.contrib.auth.signals import user_logged_in


# from django.contrib.auth.signals import user_logged_out
# from django.contrib.auth.signals import user_login_failed


@receiver(user_logged_in)
def user_login_handler(sender, request, user, **kwargs):
       

    try:
        from .tasks import send_login_email_task
        send_login_email_task.delay(user.pk) # pass id not objec
    except Exception as e:
                    # Never let email failure break registration
        print(f'Login email failed: {e}')

 

@receiver(user_signed_up)
def set_default_role(request, user, **kwargs):
    if not user.role:
        user.role = 'buyer'

    # set avarta from social account if available 
    socialaccount = kwargs.get("sociallogin")
    if socialaccount and hasattr(socialaccount, "account"):
        # for google 
        picture = socialaccount.account.extra_data.get('picture')
        if picture:
            user.avatar = picture
    user.save()


