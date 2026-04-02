FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc curl libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG CACHEBUST=3
RUN echo $CACHEBUST

COPY . .

ENV SECRET_KEY=dummy-secret-key-for-build
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost
ENV EMAIL_HOST_USER=dummy@example.com
ENV EMAIL_HOST_PASSWORD=dummy
ENV PAYSTACK_PUBLIC_KEY=dummy
ENV PAYSTACK_SECRET_KEY=dummy
ENV REDIS_URL=redis://localhost:6379
ENV DJANGO_SETTINGS_MODULE=saasproject.settings
ENV CLOUDINARY_CLOUD_NAME=dummy
ENV CLOUDINARY_API_KEY=dummy
ENV CLOUDINARY_API_SECRET=dummy
ENV CLOUDINARY_URL=dummy

RUN python manage.py collectstatic --noinput && echo "Static files collected" && ls /app/staticfiles/

RUN sed -i 's/\r//' start.sh && chmod +x start.sh

ENV PORT=10000
CMD ["/bin/bash", "start.sh"]