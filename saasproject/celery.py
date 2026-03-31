import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saasproject.settings')
 
app = Celery('saasproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 