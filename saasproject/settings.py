

from pathlib import Path
from decouple import config, Csv

from datetime import timedelta
import os
import dj_database_url



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# Application definition

INSTALLED_APPS = [
        'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channels', 
    # 'django_celery_beat', 
    'accounts', 'shop', 'cart','orders','notifications',

    # allauth apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # social providier I want are 

    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',


    #rest, cors 
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]




# pip install django-redis
# pip install channels channels-redis daphne


SITE_ID = 1 

# auth backend 

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)


# authaccount setting 


ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

ACCOUNT_USER_MODEL_USERNAME_FIELD ="username"
ACCOUNT_EMAIL_VERIFICATION = "optional"
LOGOUT_REDIRECT = '/'
# LOGIN_URL = '/accounts/login/'
LOGIN_URL = 'account_login'  # very important for allauth
# LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# for allauh add to middlware allauth.account.middleware.AccountMiddleware


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', #CORS
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shop.middleware.CartMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]





# REST FRAMEWORK 




REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}




SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,
    'BLACKLIST_AFTER_ROTATION': True,
}
 
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',   # React/Vue dev server
    'https://myapp.com',
]








# settings.
# 
REDIS_URL = config('REDIS_URL', default='redis://127.0.0.1:6379')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{REDIS_URL}/1',
        
    }
}


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
 


ASGI_APPLICATION = 'saasproject.asgi.application'
 

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG':  {'hosts': [('127.0.0.1', 6379)]},
#     }
# }
 
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [REDIS_URL]},
        'ssl_cert_reqs': None,  # for Upstash TLS

    },

}

import ssl

CELERY_BROKER_URL = f'{REDIS_URL}/0'
CELERY_RESULT_BACKEND = f'{REDIS_URL}/0'


# Required for Upstash TLS (rediss://)
CELERY_BROKER_USE_SSL = {'ssl_cert_reqs': ssl.CERT_NONE}
CELERY_REDIS_BACKEND_USE_SSL = {'ssl_cert_reqs': ssl.CERT_NONE}



# END




ROOT_URLCONF = 'saasproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.shop_context',
                'shop.context_processors.categories'

            ],
        },
    },
]

WSGI_APPLICATION = 'saasproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }




DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/



STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_ROOT =  BASE_DIR / 'media'
MEDIA_URL = '/media/'

# use this in dev  static_root works in
STATICFILES_DIRS = [BASE_DIR / 'static'] if os.path.isdir(BASE_DIR / 'static') else []



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# celry



CELERY_ACCEPT_CONTENT   = ['json']
CELERY_TASK_SERIALIZER  = 'json'
CELERY_RESULT_SERIALIZER= 'json'
CELERY_TIMEZONE         = 'UTC'
 
 
AUTH_USER_MODEL = 'accounts.CustomUser'






 
# settings.py — PRODUCTION (Gmail SMTP)
EMAIL_BACKEND     = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST        = 'smtp.gmail.com'
EMAIL_PORT        = 587
EMAIL_USE_TLS     = True
EMAIL_HOST_USER   = config('EMAIL_HOST_USER', default='')   # from .env
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# app_password = tpni qogy awrp vmup

DEFAULT_FROM_EMAIL = 'oplues01@gmail.com'





 
SECRET_KEY  = config('SECRET_KEY')
DEBUG       = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())
 
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
 

PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY', default='') 

PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY', default='')





