web: daphne -b 0.0.0.0 -p 10000 saasproject.asgi:application
worker: celery -A saasproject worker -l info
beat: celery -A saasproject beat -l info