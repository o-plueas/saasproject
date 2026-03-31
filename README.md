

Vendor Marketplace (Django E-commerce Platform)

A production-ready multi-vendor e-commerce platform built with Django, featuring real-time updates, asynchronous background processing, REST APIs, and secure authentication.



What Makes This Project Stand Out

This project goes beyond basic CRUD and demonstrates real-world backend engineering skills.


Real-time features using WebSockets powered by Django Channels abd redis
Background task processing with Celery and Redis
Secure authentication with JSON Web Token
Payment integration using Paystack
RESTful APIs using Django REST Framework



Features

User Features

User registration and login using JWT and session-based authentication
Add to cart using AJAX and Fetch API
Real-time Welcome, Login and order confirmation Email messaging
Secure checkout with Paystack
Order history 
Notifications system using WebSocket powered by Django Channels and Redis

Vendor Features

Vendor dashboard
Product management with full CRUD functionality
Inventory tracking
Order management

Advanced System Features

Real-time notifications using WebSockets
Background email tasks using Celery workers
Scheduled jobs with Celery Beat
Redis caching for performance
API endpoints for frontend or mobile integration
Secure CORS configuration



Tech Stack

Backend

Django
Django REST Framework
Django Channels
Django Web Socket 
Async and Realtime

Celery
Redis
Docker 


Frontend

HTML, CSS, JavaScript using Fetch API

Database

SQLite or PostgreSQL

Authentication

JWT using SimpleJWT
Django Allauth

Payments

Paystack



Key Packages Used

channels, channels_redis, daphne for WebSockets
celery, django-celery-beat, redis for asynchronous tasks
djangorestframework and simplejwt for APIs and authentication
Paystack for payments
django-allauth for authentication
django-cors-headers for API security



Installation

```bash
git clone https://github.com/yourusername/vendor-shop.git
cd vendor-shop

python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```



Running Services (Important)

Start Redis

```bash
redis-server
```

Run Celery Worker

```bash
celery -A your_project worker -l info
```

Run Celery Beat for scheduled tasks

```bash
celery -A your_project beat -l info
```

Run Daphne for Channels

```bash
daphne -b 0.0.0.0 -p 8000 your_project.asgi:application
```



API Endpoints (Sample)

/api/products/
/api/cart/
/api/orders/
/api/token/ for JWT login



Challenges and Engineering Decisions

Problem: Slow response when sending emails
Solution: Offloaded email sending to Celery background workers

Problem: Need real-time cart updates
Solution: Implemented WebSockets using Django Channels

Problem: Secure API authentication
Solution: Used JWT with SimpleJWT



Live Demo

Add your deployed link here



Screenshots

Homepage
Product listing
Cart
Vendor dashboard
Checkout



Contact

Email: [ugwuogochukwu01@gmail.com](mailto:ugwuogochukwu01@gmail.com)



Hiring Note

I built this project to simulate real-world production systems and improve my backend engineering skills.

I am currently open to junior backend developer roles and Django developer roles.
