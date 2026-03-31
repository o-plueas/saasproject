# notifications/utils.py  ← create this file
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification



def send_notification(user_id, title, message, notification_type='info'):
    # save to db 
    Notification.objects.create(
        user_id=user_id,
        title=title,
        message=message,
        notify_type=notification_type,
    )
  
  
      # ✅ then push via WebSocket

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{user_id}_notifications',
        {
            'type': 'notification_message',
            'title': title,
            'message': message,
            'notification_type': notification_type,
        }
    )