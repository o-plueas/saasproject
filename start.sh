#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput 2>&1
echo "Migration done"

echo "Checking storage backend..."
python manage.py shell -c "from django.core.files.storage import default_storage; print('STORAGE:', default_storage.__class__)"

echo "Creating superuser..."
python manage.py createsuperuser --noinput || echo "Superuser already exists"

echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-10000} saasproject.asgi:application