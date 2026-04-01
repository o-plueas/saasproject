#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput 2>&1

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='oplues01@gmail.com').exists():
    User.objects.create_superuser('admin', 'oplues01@gmail.com', 'qazx1234')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-10000} saasproject.asgi:application