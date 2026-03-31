#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Celery worker..."
celery -A saasproject worker --uid=nobody -l info &

echo "Starting Celery worker..."
celery -A saasproject worker --concurrency=1 --uid=nobody -l info &

echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-10000} saasproject.asgi:application