web: daphne -b 0.0.0.0 -p 10000 your_project.asgi:application
worker: celery -A your_project worker -l info
beat: celery -A saasproject beat -l info