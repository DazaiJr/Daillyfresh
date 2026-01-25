from .base import *

DEBUG = False

ALLOWED_HOSTS = ['daillyfresh.com'] 

# Production Database (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'daillyfresh_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}