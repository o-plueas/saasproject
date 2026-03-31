# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count  = notifications.filter(is_read=False).count()

    data = [
        {
            'id':      n.id,
            'title':   n.title,
            'message': n.message,
            'type':    n.notify_type,
            'is_read': n.is_read,
            'time':    n.created_at.strftime('%b %d, %H:%M'),
        }
        for n in notifications
    ]
    return JsonResponse({'notifications': data, 'unread_count': unread_count})


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})