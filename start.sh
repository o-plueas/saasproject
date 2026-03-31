#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Celery worker..."
celery -A saasproject worker -l info &

echo "Starting Celery beat..."
celery -A saasproject beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-10000} saasproject.asgi:application