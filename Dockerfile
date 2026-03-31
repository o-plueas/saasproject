FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc curl libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Dummy env vars just for collectstatic during build
ENV SECRET_KEY=dummy-secret-key-for-build
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost
ENV EMAIL_HOST_USER=dummy@example.com
ENV EMAIL_HOST_PASSWORD=dummy
ENV PAYSTACK_PUBLIC_KEY=dummy
ENV PAYSTACK_SECRET_KEY=dummy
ENV REDIS_URL=redis://localhost:6379
ENV DJANGO_SETTINGS_MODULE=saasproject.settings

RUN python manage.py collectstatic --noinput

RUN chmod +x start.sh

ENV PORT=10000
CMD ["./start.sh"]