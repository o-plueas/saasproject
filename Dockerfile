# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y gcc curl libpq-dev

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port for Render (Render assigns 10000 by default)
ENV PORT 10000

# Run Daphne server for Channels
CMD ["daphne", "-b", "0.0.0.0", "-p", "10000", "saasproject.asgi:application"]