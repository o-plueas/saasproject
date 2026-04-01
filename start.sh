#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput 2>&1
echo "Migration done"

echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-10000} saasproject.asgi:application