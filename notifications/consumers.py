
 
# notifications/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
 	
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()  # reject unauthenticated
            return
 
        # Each user has their own notification group
        self.group_name = f'user_{self.scope["user"].pk}_notifications'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
 
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
 
    # Called by channel layer when 'notification.message' event is sent
    async def notification_message(self, event):
        await self.send(text_data=json.dumps({
            'type':    event['notification_type'],
            'title':   event['title'],
            'message': event['message'],
        }))
 




