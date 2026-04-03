

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
git clone https://github.com/o-plueas/saasproject.git
cd saasproject

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
celery -A saasproject worker -l info
```

Run Celery Beat for scheduled tasks

```bash
celery -A saasproject beat -l info
```

Run Daphne for Channels

```bash
daphne -b 0.0.0.0 -p 8000 saasproject.asgi:application
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
Solution: Used fetch api to implement realtime update

Problem: Need realtime notification
Solution: Implemented WebSockets using Django Channels

Problem: Secure API authentication
Solution: Used JWT with SimpleJWT


Live Demo

https://youtu.be/8GnVtF7GqUI

Screenshots

Homepage (No login)
https://drive.google.com/file/d/1BH6CfgzYApNZG0QijcbOdKCD56zBRZvg/view?usp=drive_link


Product listing
https://drive.google.com/file/d/1hKSO9FqRijAsSzQzPXWdeR1Mc8XQk35s/view?usp=drive_link

Cart

ps://drive.google.com/file/d/1PHwgqdK_rJSuTs3SItJ634YsncEByQfB/view?usp=drive_link

Order Form
https://drive.google.com/file/d/1FqPLUI4fO_3fzV1nz3nQ4-FfC6bPfAU0/view?usp=drive_link

Checkout
https://drive.google.com/file/d/1kaReJ3qUiItnpp7R0VOxTCjfSunL72IH/view?usp=drive_link

Vendor dashboard
https://drive.google.com/file/d/13W_DGWq_rWWqswxlV8mhyf1Bx0wTsaeL/view?usp=drive_link



Contact

Email: 
ugwuogochukwu01@gmail.com 

LinkedIn:
www.linkedin.com/in/ogochukwu-lucy-ugwu



Hiring Note

I built this project to simulate real-world production systems and improve my backend engineering skills.

I am currently open to junior backend developer roles and Django developer roles.
